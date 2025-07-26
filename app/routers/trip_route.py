from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.trip_extraction_service import (
    validate_user_input,
    generate_trip_json,
    parse_trip_data,
)

router = APIRouter()

# 🔹 Define a request model for the JSON body
class PromptRequest(BaseModel):
    prompt: str

@router.post("/extract-info")
async def extract_trip_from_input(request: PromptRequest):
    if not validate_user_input(request.prompt):
        raise HTTPException(
            status_code=400,
            detail=(
                "⚠️ Please provide more detail. Try including:\n"
                "- Where you're going\n"
                "- How long the trip is\n"
                "- What you're interested in (music, food, etc.)\n"
                "- Your travel style (relaxing, adventurous, etc.)"
            ),
        )

    json_str = generate_trip_json(request.prompt)

    try:
        trip = parse_trip_data(json_str)
        return trip
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
