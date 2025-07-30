from datetime import datetime
from uuid import UUID as PyUUID
from sqlalchemy import JSON, UUID, Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class UserHistory(Base):
    __tablename__ = "user_history"

    
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    prompt = Column(Text, nullable=False)
    destination = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    tastes = Column(Text, nullable=True)
    style = Column(Text, nullable=True)

    generated_itinerary = Column(Text, nullable=False)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


#   CREATE TABLE user_history (
#     id UUID PRIMARY KEY NOT NULL,
#     prompt TEXT NOT NULL,
#     destination VARCHAR,
#     duration VARCHAR,
#     tastes TEXT,
#     style TEXT,
#     generated_itinerary TEXT,
#     user_id UUID NOT NULL REFERENCES users(id),
#     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
#     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
# );