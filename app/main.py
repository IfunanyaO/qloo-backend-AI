from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Routers
from app.routers import auth as auth_router, trip_route
from app.routers import culturetrip_route
from app.routers import itinerary_route
# End of routers

import logging

from app.shared.errors import AppError

# Initialize app
app = FastAPI(
    title="FastAPI + MySQL Starter",
    description="A sample FastAPI app with MySQL and modular structure",
    version="1.0.0",
)

# Create the main API router with a shared prefix
api_router = APIRouter(prefix="/api/v1")

# CORS settings (allow all for now; restrict in production)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://www.devphilip.com"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Custom error handler
@app.exception_handler(AppError)
async def app_exception_handler(_: Request, err: AppError):
    return JSONResponse(
        status_code=err.status_code,
        content={"detail": err.message},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error occurred on path {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
        },
    )


# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI + MySQL 🚀"}




# Register your sub-routers to the main router
api_router.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
api_router.include_router(culturetrip_route.router, prefix="/ct-planner", tags=["Culture Trip Enpoints"])
api_router.include_router(trip_route.router, prefix="/trip", tags=["Validate User Input request Enpoints"])
api_router.include_router(itinerary_route.router, prefix="/endpoint", tags=["Itinerary"])

# Include the main API router into your FastAPI app. This should be at the bottom of the api_router
app.include_router(api_router)

