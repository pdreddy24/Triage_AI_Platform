from datetime import datetime, UTC
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import declarative_base
import uuid


Base = declarative_base()


class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    transaction_id = Column(String, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_band = Column(String, nullable=False)
    route_to = Column(String, nullable=False)

    status = Column(String, default="OPEN", nullable=False)
    assigned_to = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False
    )