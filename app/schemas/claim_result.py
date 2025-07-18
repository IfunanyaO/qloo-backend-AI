from pydantic import BaseModel, UUID4
from typing import Any
from uuid import UUID  # <-- this accepts all UUID versions

class ClaimResultIn(BaseModel):
    claim_id: UUID
    claim: str
    verdict_data: dict
    user_id: UUID  # changed from UUID4 to UUID

class ClaimResultOut(BaseModel):
    claim_id: UUID
    claim: str
    verdict_data: dict
    user_id: UUID

    class Config:
        orm_mode = True  # allows returning ORM objects from SQLAlchemy