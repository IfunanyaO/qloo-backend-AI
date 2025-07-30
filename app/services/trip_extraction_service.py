import json
import openai
from pydantic import ValidationError
from app.schemas.tripdata import TripData
from dotenv import load_dotenv
load_dotenv()
import os



client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def validate_user_input(user_input: str) -> bool:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "Determine if the user's input contains enough information to generate a personalized travel itinerary. "
                    "It must include: a destination, a trip duration, at least one interest (like food, music, fashion), and a travel style (e.g., relaxing, adventurous). "
                    "Respond ONLY with true or false."
                )
            },
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content.strip().lower() == "true"


def generate_trip_json(user_input: str, openAI_model:str) -> str:
    response = client.chat.completions.create(
        model=openAI_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract structured trip data from user input. "
                    "Return JSON with keys: destination (string), duration (string), tastes (list of strings), and style (list of strings). "
                    "Output JSON only."
                )
            },
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content


def parse_trip_data(json_str: str, original_prompt: str) -> TripData:
    try:
        structured = json.loads(json_str)
        structured["original_prompt"] = original_prompt  # Inject the original prompt
        return TripData(**structured)
    
    except (ValidationError, json.JSONDecodeError) as e:
        raise ValueError(
            "Invalid trip structure. Please include destination, duration, tastes, and travel style."
        ) from e
