from fastapi import FastAPI
from services.climate import get_air_quality, get_hotspots


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


# -----------------------------------
# POLLUTION HOTSPOTS
# -----------------------------------

@app.get("/api/hotspots")
def hotspots():

    return {
        "hotspots": get_hotspots()
    }


# -----------------------------------
# AIR QUALITY SPIKE PREDICTION
# -----------------------------------

@app.get("/api/prediction/{city}")
def prediction(city: str):

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

    pm25 = result["pm25"]
    humidity = result["humidity"]
    temperature = result["temperature"]

    # Prototype prediction score
    risk_score = 0

    # PM2.5 contribution
    if pm25 >= 75:
        risk_score += 50
    elif pm25 >= 50:
        risk_score += 30
    else:
        risk_score += 10

    # Temperature contribution
    if temperature >= 35:
        risk_score += 20
    elif temperature >= 30:
        risk_score += 10

    # Humidity contribution
    if humidity < 45:
        risk_score += 10

    # Prediction category
    if risk_score >= 60:
        prediction_result = "HIGH POSSIBILITY OF AIR QUALITY SPIKE"

    elif risk_score >= 35:
        prediction_result = "MODERATE POSSIBILITY OF AIR QUALITY SPIKE"

    else:
        prediction_result = "LOW POSSIBILITY OF AIR QUALITY SPIKE"

    return {
        "city": city,
        "current_pm25": pm25,
        "temperature": temperature,
        "humidity": humidity,
        "risk_score": risk_score,
        "prediction": prediction_result
    }
