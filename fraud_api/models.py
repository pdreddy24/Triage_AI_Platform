# services/fraud_api/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class UploadBatch(Base):
    __tablename__ = "upload_batches"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    filename = Column(String)
    s3_key = Column(String)
    status = Column(String, default="processing")
    total_rows = Column(Integer, default=0)
    success_rows = Column(Integer, default=0)
    failed_rows = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TransactionRecord(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(String, index=True)
    transaction_id = Column(String)
    user_id = Column(String)
    amount = Column(Float)
    merchant = Column(String)
    fraud_score = Column(Float, nullable=True)
    graph_risk = Column(Float, nullable=True)
    is_valid = Column(Boolean, default=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())