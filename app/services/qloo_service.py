import os
from dotenv import load_dotenv
load_dotenv()
import httpx
from fastapi import HTTPException



QLOO_API_KEY = os.getenv("QLOO_API_KEY")
QLOO_BASE_URL = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com")

async def get_insight(endpoint: str) -> dict:
    if not QLOO_API_KEY:
        raise HTTPException(status_code=500, detail="Qloo API key not found in environment variables.")

    headers = {
        "X-Api-Key": QLOO_API_KEY
    }

    url = f"{QLOO_BASE_URL}/v2{endpoint}"
    print(url)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Qloo API Error: {response.text}"
                )

            return response.json()

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
