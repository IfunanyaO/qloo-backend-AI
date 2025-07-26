from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.llm_service import generate_itinerary
from app.services.qloo_service import get_insight


router = APIRouter()

# 🔹 Define expected input format
class TripPlanRequest(BaseModel):
    destination: str
    duration: str
    tastes: List[str] # e.g., ["jazz", "seafood", "indie"]
    style: List[str]

@router.get("/test-endpoint")
def read_root():
    return {"message": "Welcome to FastAPI + Qloo 🚀"}


@router.post("/plan-trip")
async def plan_trip(payload: TripPlanRequest):
    destination = payload.destination
    tastes = payload.tastes
    style = payload.style
    duration = payload.duration

    if not destination or not tastes:
        raise HTTPException(status_code=400, detail="Both 'destination' and at least one 'taste' are required.")

    try:
        all_places = []
        heatmap_neighborhoods = []
        demographics_summary = []
        related_tags = []  # optional: if you want to enrich later

        for taste in tastes:
            tag = f"urn:tag:genre:{taste}"

            # Basic insights: place recommendations
            basic = await get_insight(
                f"/insights/?filter.type=urn:entity:place&signal.interests.tags={tag}&filter.location.query={destination}"
            )
            taste_places = [place.get("name") for place in basic.get("data", [])]
            all_places.extend([{"name": p} for p in taste_places])

            # Demographics: summarize affinity by age/gender
            demographics = await get_insight(
                f"/insights/?filter.type=urn:demographics&signal.interests.tags={tag}"
            )
            if "data" in demographics:
                summary = f"For taste '{taste}': " \
                          + ", ".join([f"{g['group']}s score {g['score']:.2f}" for g in demographics.get("data", {}).get("age", [])])
                demographics_summary.append(summary)

            # Heatmap: get high-affinity neighborhoods
            heatmap = await get_insight(
                f"/insights/?filter.type=urn:heatmap&filter.location.query={destination}&signal.interests.tags={tag}"
            )
            heatmap_points = heatmap.get("data", {}).get("points", [])
            heatmap_neighborhoods.extend([f"Lat:{pt['location']['latitude']:.4f}, Lon:{pt['location']['longitude']:.4f}" for pt in heatmap_points[:3]])

        # Call the LLM itinerary builder
        itinerary = generate_itinerary(
            destination=destination,
            duration=duration,
            tastes=tastes,
            style=style,
            qloo_places=all_places,
            demographics_summary="\n".join(demographics_summary),
            related_tags=related_tags,  # optional
            heatmap_neighborhoods=heatmap_neighborhoods
        )

        return {
            "destination": destination,
            "tastes": tastes,
            "style": style,
            "duration": duration,
            "itinerary": itinerary
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# @router.post("/plan-trip")
# async def plan_trip(payload: TripPlanRequest):
#     destination = payload.destination
#     tastes = payload.tastes

#     if not destination or not tastes:
#         raise HTTPException(status_code=400, detail="Both 'destination' and at least one 'taste' are required.")

#     try:
#         # Combine all results from Qloo based on each taste
#         all_basic_insights = []
#         all_demographics = []
#         all_heatmaps = []

#         for taste in tastes:
#             tag = f"urn:tag:genre:{taste}"

#             basic = await get_insight(
#                 f"/insights/?filter.type=urn:entity:place&signal.interests.tags={tag}&filter.location.query={destination}"
#             )
#             demographics = await get_insight(
#                 f"/insights/?filter.type=urn:demographics&signal.interests.tags={tag}"
#             )
#             heatmap = await get_insight(
#                 f"/insights/?filter.type=urn:heatmap&filter.location.query={destination}&signal.interests.tags={tag}"
#             )

#             all_basic_insights.append({taste: basic})
#             all_demographics.append({taste: demographics})
#             all_heatmaps.append({taste: heatmap})

#         return {
#             "destination": destination,
#             "tastes": tastes,
#             "insights": {
#                 "basic": all_basic_insights,
#                 "demographics": all_demographics,
#                 "heatmap": all_heatmaps
#             }
#         }

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# @router.post("/plan-trip")
# async def plan_trip(payload: dict):
#     destination = payload.get("destination")
#     taste = payload.get("taste")

#     if not destination or not taste:
#         raise HTTPException(status_code=400, detail="Missing required fields: destination or taste")

#     try:
#         # taste_analysis = await get_insight(f"/taste-analysis?type=tag&id=urn:tag:genre:{taste}")
#         # demographics = await get_insight(f"/insights/?filter.type=urn:demographics&signal.interests.tags=urn:tag:genre:{taste}")
#         # heatmap = await get_insight(f"/insights/?filter.type=urn:heatmap&filter.location.query={destination}&signal.interests.tags=urn:tag:genre:{taste}")
#         # location = await get_insight(f"/insights/?filter.type=urn:entity:place&filter.location.query={destination}")
#         basic = await get_insight(f"/insights/?filter.type=urn:entity:place&signal.interests.tags=urn:tag:genre:{taste}&filter.location.query={destination}")
#     except HTTPException as e:
#         raise e  # re-raise any upstream Qloo API error

#     return {
#         # "taste_analysis": taste_analysis,
#         # "demographics": demographics,
#         # "heatmap": heatmap,
#         # "location_insights": location,
#         "basic_insights": basic
#     }
