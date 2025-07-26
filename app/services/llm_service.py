# services/llm_service.py

from openai import OpenAI
from typing import List
from dotenv import load_dotenv
load_dotenv()
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_itinerary(
    destination: str,
    duration: str,
    tastes: List[str],
    style: List[str],
    qloo_places: List[dict] = None,
    demographics_summary: str = "",
    related_tags: List[str] = [],
    heatmap_neighborhoods: List[str] = []
) -> str:
    qloo_places = qloo_places or []

    map_links = "\n".join([
        f"- {place['name']} 📍 [Map](https://www.google.com/maps/search/?api=1&query={place['name'].replace(' ', '+')}+{destination})"
        for place in qloo_places
    ])

    prompt = f"""
You are a culturally intelligent AI travel assistant.

Generate a {duration} itinerary for a trip to {destination} based on:

Travel Style: {', '.join(style)}
Tastes: {', '.join(tastes)}

Qloo Insights:
- Demographics: {demographics_summary or "Not provided"}
- Related Tags: {', '.join(related_tags) or "None"}
- Heatmap Hints: Focus on areas like: {', '.join(heatmap_neighborhoods) or "not specified"}
- Places to include:
{map_links or "No specific places"}

Return a daily breakdown with **morning, afternoon, and evening**. Include cultural activities, food/music recs, and a 📍 Google Maps link. End with a vibe-themed shareable summary.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a culturally intelligent travel planner."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
