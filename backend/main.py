from fastapi import FastAPI
from services.climate import get_air_quality

app = FastAPI(
    title="AirTrace AI",
    description="AI-powered climate and air-quality intelligence platform",
    version="1.0.0"
)


# -----------------------------------
# HOME
# -----------------------------------

@app.get("/")
def home():
    return {
        "message": "AirTrace AI backend is running"
    }


# -----------------------------------
# HEALTH CHECK
# -----------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -----------------------------------
# AIR QUALITY BY CITY
# -----------------------------------

@app.get("/api/air-quality/{city}")
def air_quality(city: str):

    result = get_air_quality(city)

    if result is None:
        return {
            "error": "City not found",
            "available_cities": [
                "Delhi",
                "Mumbai",
                "Kolkata",
                "Bengaluru",
                "Hyderabad"
            ]
        }

    return result