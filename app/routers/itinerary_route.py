from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.prompt_request import PromptRequest
from app.services.trip_extraction_service import generate_trip_json, parse_trip_data
from app.services.qloo_service import get_insight
from app.services.llm_service import generate_itinerary

router = APIRouter()

@router.post("/plan-trip")
async def plan_trip(request: PromptRequest):
    prompt = request.prompt
    print("📩 Received prompt:", prompt)

    try:
        # 🔹 Step 1: Extract structured trip JSON from prompt
        json_str = generate_trip_json(prompt)
        print("✅ Extracted JSON from LLM:", json_str)

        # 🔹 Step 2: Parse structured data into Pydantic model
        trip = parse_trip_data(json_str)
        print("✅ Parsed trip data:", trip)

        destination = trip.destination
        duration = trip.duration
        tastes = trip.tastes
        style = trip.style

        print(f"🗺️ Destination: {destination} | ⏳ Duration: {duration}")
        print(f"🎨 Tastes: {tastes} | 🧘 Style: {style}")

        all_places = []
        heatmap_neighborhoods = []
        demographics_summary = []

        # 🔹 Step 3: Fetch Qloo insights for each taste
        for taste in tastes:
            print(f"\n🔍 Processing taste: {taste}")
            tag = f"urn:tag:genre:{taste}"

            # Basic insights
            basic = await get_insight(
                f"/insights/?filter.type=urn:entity:place&signal.interests.tags={tag}&filter.location.query={destination}"
            )
            # print(f"📍 Basic insights for '{taste}':", basic)
            print(f"📍 Basic insights")
            taste_places = [place.get("name") for place in basic.get("data", [])]
            all_places.extend([{"name": p} for p in taste_places])

            # Demographics
            demographics = await get_insight(
                f"/insights/?filter.type=urn:demographics&signal.interests.tags={tag}"
            )
            # print(f"👥 Demographics for '{taste}':", demographics)
            print(f"👥 Demographics for")
            if "data" in demographics:
                summary = f"For taste '{taste}': " + ", ".join([
                    f"{g['group']}s score {g['score']:.2f}"
                    for g in demographics.get("data", {}).get("age", [])
                ])
                demographics_summary.append(summary)

            # Heatmap
            heatmap = await get_insight(
                f"/insights/?filter.type=urn:heatmap&filter.location.query={destination}&signal.interests.tags={tag}"
            )
            # print(f"🌡️ Heatmap for '{taste}':", heatmap)
            print(f"🌡️ Heatmap for ")
            heatmap_points = heatmap.get("data", {}).get("points", [])
            heatmap_neighborhoods.extend([
                f"Lat:{pt['location']['latitude']:.4f}, Lon:{pt['location']['longitude']:.4f}"
                for pt in heatmap_points[:3]
            ])

        # 🔹 Step 4: Generate the itinerary with LLM
        print("\n🧠 Calling LLM with aggregated insights...")
        itinerary = generate_itinerary(
            destination=destination,
            duration=duration,
            tastes=tastes,
            style=style,
            qloo_places=all_places,
            demographics_summary="\n".join(demographics_summary),
            heatmap_neighborhoods=heatmap_neighborhoods
        )
        # print("📅 Generated itinerary:\n", itinerary)
        print("📅 Generated itinerary")

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
