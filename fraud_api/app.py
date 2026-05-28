# services/fraud_api/app.py

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import csv
import io
import asyncio

from .database import SessionLocal
from .models import UploadBatch, TransactionRecord
from .schemas import TransactionSchema
from .s3 import upload_to_s3
from .auth import get_current_tenant
from .config import settings

app = FastAPI(title="Fraud API - Enterprise Upload Service")


# ==========================================================
# FILE UPLOAD ENDPOINT
# ==========================================================

@app.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    tenant_id: str = Depends(get_current_tenant),
):

    contents = await file.read()

    # 1️⃣ FILE SIZE LIMIT
    if len(contents) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large")

    # 2️⃣ SAVE TO S3
    s3_key = f"{tenant_id}/{file.filename}"
    await upload_to_s3(contents, s3_key)

    # 3️⃣ CREATE BATCH RECORD
    async with SessionLocal() as session:
        batch = UploadBatch(
            tenant_id=tenant_id,
            filename=file.filename,
            s3_key=s3_key,
        )
        session.add(batch)
        await session.commit()
        await session.refresh(batch)

    # 4️⃣ BACKGROUND PROCESSING
    background_tasks.add_task(process_csv, contents, tenant_id, batch.id)

    return {
        "batch_id": batch.id,
        "status": "processing"
    }


# ==========================================================
# BACKGROUND CSV PROCESSING
# ==========================================================

async def process_csv(contents: bytes, tenant_id: str, batch_id: int):

    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    total = success = failed = 0

    async with SessionLocal() as session:

        for row in reader:
            total += 1

            try:
                # 5️⃣ SCHEMA VALIDATION
                tx = TransactionSchema(**row)

                record = TransactionRecord(
                    tenant_id=tenant_id,
                    transaction_id=tx.transaction_id,
                    user_id=tx.user_id,
                    amount=tx.amount,
                    merchant=tx.merchant,
                    is_valid=True
                )
                success += 1

            except Exception as e:
                record = TransactionRecord(
                    tenant_id=tenant_id,
                    transaction_id=row.get("transaction_id"),
                    is_valid=False,
                    error_message=str(e)
                )
                failed += 1

            session.add(record)

        # 6️⃣ PARTIAL FAILURE SUPPORT
        batch = await session.get(UploadBatch, batch_id)
        batch.total_rows = total
        batch.success_rows = success
        batch.failed_rows = failed
        batch.status = "completed"

        await session.commit()
@app.get("/batch/{batch_id}")
async def get_batch(batch_id: int, tenant_id: str = Depends(get_current_tenant)):
    async with SessionLocal() as session:
        batch = await session.get(UploadBatch, batch_id)

        if not batch or batch.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Not found")

        return {
            "status": batch.status,
            "total_rows": batch.total_rows,
            "success_rows": batch.success_rows,
            "failed_rows": batch.failed_rows,
        }