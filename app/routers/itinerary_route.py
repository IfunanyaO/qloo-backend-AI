from fastapi import APIRouter, HTTPException
import httpx
from pydantic import BaseModel
from app.database import async_session_maker
from app.dependencies import get_db
from app.routers.student_route import save_user_itinerary
from app.schemas.prompt_request import PromptRequest
from app.services.trip_extraction_service import generate_trip_json, parse_trip_data
from app.services.qloo_service import get_insight
from app.services.llm_service import fetch_weather_forecast, generate_itinerary
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

@router.post("/plan-trip")
async def plan_trip(request: PromptRequest):
    prompt = request.prompt
    print("📩 Received prompt:", prompt)

    try:
        # 🔹 Step 1: Extract structured trip JSON from prompt
        json_str = generate_trip_json(prompt, request.model)
        print("✅ Extracted JSON from LLM:", json_str)

        # 🔹 Step 2: Parse structured data into Pydantic model
        trip = parse_trip_data(json_str, prompt)
        print("✅ Parsed trip data:", trip)

        destination = trip.destination
        duration = trip.duration
        tastes = trip.tastes
        style = trip.style
        original_prompt = trip.original_prompt

        print(f"🗺️ Destination: {destination} | ⏳ Duration: {duration}")
        print(f"🎨 Tastes: {tastes} | 🧘 Style: {style}")

        # 🔹 Step 3: Use only the first taste
        if not tastes:
            raise HTTPException(status_code=400, detail="No tastes provided in prompt.")

        primary_taste = tastes[0]
        tag = f"urn:tag:genre:{primary_taste}"
        print(f"🔍 Fetching Qloo data for tag: {tag}")

        # 🔹 Step 4: Fetch Qloo place insights for that one taste
        basic = await get_insight(
            f"/insights/?filter.type=urn:entity:place&signal.interests.tags={tag}&filter.location.query={destination}"
        )

        # 🔹 Step 5: Fetch weather forecast
        weather_forecast = fetch_weather_forecast(destination, original_prompt)

        print(weather_forecast)
        
        # 🔹 Step 5: Generate the itinerary using basic place insights
        print("\n🧠 Calling LLM with aggregated insights...")
        itinerary = generate_itinerary(
            openAI_model=request.model,
            original_prompt=original_prompt,
            destination=destination,
            duration=duration,
            tastes=tastes,
            style=style,
            qloo_places=basic.get("results", {}).get("entities", []),
            weather_forecast=weather_forecast  # ✅ Pass this to the LLM prompt
        )
        print("📅 Generated itinerary")

        tastes_str = ", ".join(tastes)  # tastes is a list
        style_str = ", ".join(style)    # style is a list

        # Step 7: Save to PostgreSQL
        async with async_session_maker() as db:
            if getattr(request, "loggedIn", False) is True:
                print("📅 Saving User history itinerary")
                await save_user_itinerary(
                    db=db,
                    user_id=getattr(request, "sessionId", None),
                    prompt=prompt,
                    destination=destination,
                    duration=duration,
                    tastes=tastes_str,
                    style=style_str,
                    generated_itinerary=itinerary
                )

        return {
            "destination": destination,
            "tastes": tastes,
            "style": style,
            "duration": duration,
            "itinerary": itinerary
        }

    except Exception as e:
        print("❌ Error during plan-trip:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/qloo-only-trip")
async def qloo_basic_trip(request: PromptRequest):
    prompt = request.prompt
    print("📩 Received prompt:", prompt)

    try:
        # Step 1: Extract structured trip data from prompt
        json_str = generate_trip_json(prompt)
        trip = parse_trip_data(json_str)

        destination = trip.destination
        duration = trip.duration
        tastes = trip.tastes
        style = trip.style

        print(f"🗺️ Destination: {destination} | ⏳ Duration: {duration}")
        print(f"🎨 Tastes: {tastes} | 🧘 Style: {style}")

        if not tastes:
            raise HTTPException(status_code=400, detail="No tastes found in prompt")

        # Step 2: Use first taste directly
        primary_taste = tastes[0]
        tag = f"urn:tag:genre:{primary_taste.lower().replace(' ', '-')}"  # e.g., jazz music → jazz-music

        print(f"🔍 Using taste tag '{tag}'")

        # Step 3: Fetch Qloo place recommendations
        basic = await get_insight(
            f"/insights/?filter.type=urn:entity:place&signal.interests.tags={tag}&filter.location.query={destination}"
        )
        print(f"/insights/?filter.type=urn:entity:place&signal.interests.tags={tag}&filter.location.query={destination}")
        # taste_places = [place.get("name") for place in basic.get("data", [])]
        # all_places = [{"name": p} for p in taste_places]

        return {
            "destination": destination,
            "taste_used": primary_taste,
            "style": style,
            "duration": duration,
            "qloo_places":  basic.get("results", {}).get("entities", [])
        }

    except Exception as e:
        print("❌ Error during Qloo basic trip:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    
QLOO_API_KEY = os.getenv("QLOO_API_KEY")  # Make sure this is set in your .env or system env

@router.get("/test-qloo-jazz")
async def test_qloo_insight():
    url = "https://hackathon.api.qloo.com/v2/insights/"
    params = {
        "filter.type": "urn:entity:place",
        "signal.interests.tags": "urn:tag:genre:jazz",
        "filter.location.query": "Lisbon"
    }
    headers = {
        "x-api-key": QLOO_API_KEY
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print("❌ Qloo API error:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch from Qloo")