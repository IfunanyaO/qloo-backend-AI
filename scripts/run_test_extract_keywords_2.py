import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
import openai
from pydantic import ValidationError

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.schemas.tripdata import TripData

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# user_input = "I want a 5-day trip to Lisbon, into jazz music and indie bookstores, something relaxing and low budget."
user_input = "sex"  # Try this to see the validation fail

# ✅ Step 1: Pre-check with GPT (Is the prompt detailed enough?)
validation_response = client.chat.completions.create(
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

is_valid = validation_response.choices[0].message.content.strip().lower() == "true"

if not is_valid:
    print("⚠️ Please provide more detail. Try something like: I'm looking for a 4-day getaway to Kyoto, centered around traditional tea culture and nature walks, something peaceful and culturally rich. We would like to know")
    print("- Where are you going?")
    print("- How long will the trip be?")
    print("- What are your interests? (e.g., jazz, tacos, museums)")
    print("- What's your travel style? (e.g., relaxing, adventurous)")
    sys.exit()

# ✅ Step 2: Main GPT extraction
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": (
                "Extract structured trip data from user input. "
                "Return JSON with keys: destination (string), duration (string), tastes (list of strings), style (list of strings). "
                "Output JSON only."
            )
        },
        {"role": "user", "content": user_input}
    ]
)

raw_content = response.choices[0].message.content

# ✅ Step 3: Parse + Validate GPT response using Pydantic
try:
    structured = json.loads(raw_content)
    trip = TripData(**structured)
    print("✅ Valid trip extracted:", trip)
except (ValidationError, json.JSONDecodeError) as e:
    print("⚠️ GPT returned invalid structured data.")
    print("Please try again with more clearly formatted preferences.")
    print("- Destination (e.g., Lisbon)")
    print("- Duration (e.g., 5 days)")
    print("- Interests (e.g., jazz, food, bookstores)")
    print("- Style (e.g., relaxing, budget-friendly)")
