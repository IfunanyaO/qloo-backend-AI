from sqlalchemy import String, DateTime, UUID, Column, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import datetime, timezone
from uuid import UUID as PyUUID


class User(Base):
    __tablename__ = "users"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    google_id: Mapped[str] = mapped_column(String, unique=True)
    # Auto-managed timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

