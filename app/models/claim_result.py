from sqlalchemy import Column, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String, JSON
from app.database import Base
from uuid import UUID as PyUUID

class ClaimResult(Base):
    __tablename__ = "claim_results"

    claim_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    claim = Column(String, nullable=False)
    verdict_data = Column(JSON, nullable=False)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
