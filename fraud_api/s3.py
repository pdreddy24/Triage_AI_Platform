# services/fraud_api/s3.py

import aioboto3
from .config import settings

async def upload_to_s3(file_bytes: bytes, filename: str):
    session = aioboto3.Session()

    async with session.client(
        "s3",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
    ) as s3:
        await s3.put_object(
            Bucket=settings.S3_BUCKET,
            Key=filename,
            Body=file_bytes
        )

    return filename