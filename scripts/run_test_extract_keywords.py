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
# from app.services.text_normalize_service import normalize_text

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))  # Your actual key here

user_input = "I want a 5-day trip to Lisbon, into jazz music and indie bookstores, something relaxing and low budget."
# user_input = "sex"

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Extract structured trip data from user text. Return JSON with destination, duration, tastes, and style."},
        {"role": "user", "content": user_input}
    ]
)


raw_content = response.choices[0].message.content

# print(response.choices[0].message.content)
try:
    structured = json.loads(raw_content)
    trip = TripData(**structured)
    print("✅ Valid trip extracted:", trip)
except (ValidationError, json.JSONDecodeError) as e:
    # 🔔 This is where you notify the user
    print("⚠️ We couldn't understand your request.")
    print("Please try again with more detailed info like:")
    print("- Your destination")
    print("- How long the trip is")
    print("- What you're interested in (music, food, fashion, etc.)")
    print("- Your travel style (relaxing, adventurous, luxury, etc.)")