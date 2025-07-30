# services/llm_service.py
import requests
from openai import OpenAI
from typing import List
from dotenv import load_dotenv
load_dotenv()
import os
import re

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

OPENWEATHERMAP_API_KEY = os.getenv('WEATHERAPPID')

def extract_duration_days(prompt: str) -> int:
    match = re.search(r'(\d+)[-\s]*day', prompt.lower())
    return int(match.group(1)) if match else 5  # default to 5

def fetch_weather_forecast(city: str, prompt: str) -> str:
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={OPENWEATHERMAP_API_KEY}"
        )
        res = requests.get(url)
        data = res.json()
        
        if "list" not in data:
            return "Weather data unavailable."

        # Grab daily forecasts at noon (12:00:00)
        daily = [
            f"{entry['dt_txt'].split(' ')[0]}: {entry['weather'][0]['description'].title()}, "
            f"{entry['main']['temp']}°C"
            for entry in data["list"]
            if "12:00:00" in entry["dt_txt"]
        ][:extract_duration_days(prompt)]  # limit to 5 days

        return "\n".join(daily)
    
    except Exception as e:
        return f"⚠️ Error fetching weather: {str(e)}"

def generate_itinerary(
    openAI_model:str,
    original_prompt: str,
    destination: str,
    duration: str,
    tastes: List[str],
    style: List[str],
    qloo_places: List[dict] = None,
    weather_forecast: str = "",
    demographics_summary: str = "",
    related_tags: List[str] = [],
    heatmap_neighborhoods: List[str] = []
) -> str:
    qloo_places = qloo_places or []

    def format_place(place):
        name = place.get("name", "Unknown Place")
        props = place.get("properties", {})
        address = props.get("address", "")
        website = props.get("website", "")
        phone = props.get("phone", "")
        rating = props.get("business_rating")
        cost_estimate = props.get("average_cost", "Estimate not available")
        keywords = [kw["name"] for kw in props.get("keywords", [])][:3]

        details = f"""- **{name}**
  📍 [Map it](https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}+{destination})
  {'📞 ' + phone if phone else ''}
  {'🌐 ' + website if website else ''}
  {'⭐ Rating: ' + str(rating) if rating else ''}
  {'💸 Estimated cost: ' + str(cost_estimate) if cost_estimate else ''}
  {'🔑 Keywords: ' + ', '.join(keywords) if keywords else ''}
"""
        return details

    formatted_places = "\n".join([format_place(place) for place in qloo_places]) or "No recommended places available."

    print("Olamide")
    # print(formatted_places)
    # print(weather_forecast)
    # Compose the GPT prompt
    prompt = f"""
You are a culturally intelligent travel planner.

A user said: "{original_prompt}"

Create a personalized **{duration}** itinerary for a trip to **{destination}**. The traveler prefers:

**Tastes**: {', '.join(tastes)}
**Travel Style**: {', '.join(style)}

**Weather Forecast**:
{weather_forecast or "No forecast available."}

Use the following place insights to plan activities. Include them in appropriate time slots (morning, afternoon, evening):

{formatted_places}

Also consider:
- **Demographics**: {demographics_summary or "N/A"}
- **Related Tags**: {', '.join(related_tags) or "N/A"}
- **Hotspots**: {', '.join(heatmap_neighborhoods) or "N/A"}

For each day:
- Suggest a **morning**, **afternoon**, and **evening** activity
- Use the **weather forecast** to let the traveler know how to dress for the expected weather conditions each day
- When using any of the recommended places, **reuse their full details including the map link, phone, website, rating, cost estimate, and keywords** as available
- Mention if a place has a **high rating**, **website**, or **keywords** that align with tastes
- Add a **rough cost range** or say "budget-friendly" if unknown
- Suggest ideal times to go if it's a meal place, music venue, bookstore, etc.
- Incorporate additional cues from the original prompt

End with a short, stylish **trip summary caption** (Instagram-worthy).

Make it fun, detailed, and personalized!
"""

    response = client.chat.completions.create(
        model=openAI_model,
        messages=[
            {"role": "system", "content": "You are a culturally intelligent travel planner that creates rich, fun, and personalized itineraries."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
