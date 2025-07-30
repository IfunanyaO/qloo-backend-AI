from pydantic import BaseModel, ValidationError
from typing import List

class TripData(BaseModel):
    destination: str
    duration: str
    tastes: List[str]
    style: List[str]
    original_prompt: str 