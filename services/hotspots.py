from services.climate import get_air_quality


# Temporary in-memory storage
# Later we will replace this with a database.
CITIZEN_REPORTS = []


def add_citizen_report(report):
    """
    Store a citizen pollution report temporarily.
    """

    CITIZEN_REPORTS.append(report)

    return report


def get_citizen_reports():
    """
    Return all citizen reports.
    """

    return CITIZEN_REPORTS


def calculate_hotspot_intelligence():
    """
    Combine environmental data and citizen reports
    to identify potential pollution hotspots.
    """

    hotspots = []

    # ==========================================
    # PART 1: ENVIRONMENTAL HOTSPOTS
    # ==========================================

    cities = [
        "Delhi",
        "Mumbai",
        "Kolkata",
        "Bengaluru",
        "Hyderabad"
    ]

    for city in cities:

        air_data = get_air_quality(city)

        if air_data is None:
            continue

        pm25 = air_data["pm25"]

        # Environmental risk
        if pm25 >= 75:

            environmental_risk = "VERY HIGH"

        elif pm25 >= 50:

            environmental_risk = "HIGH"

        elif pm25 >= 35:

            environmental_risk = "MODERATE"

        else:

            environmental_risk = "LOW"


        # Only consider moderate or higher risk
        if environmental_risk in [
            "VERY HIGH",
            "HIGH",
            "MODERATE"
        ]:

            hotspots.append({

                "city": city,

                "latitude": None,

                "longitude": None,

                "risk": environmental_risk,

                "pm25": pm25,

                "citizen_reports": 0,

                "evidence": [
                    f"PM2.5 level: {pm25}"
                ],

                "source": "Environmental data",

                "recommended_action": (
                    "Monitor local air-quality conditions "
                    "and investigate potential pollution sources."
                )
            })


    # ==========================================
    # PART 2: CITIZEN REPORT INTELLIGENCE
    # ==========================================

    for report in CITIZEN_REPORTS:

        city = report["city"]

        description = report["description"].lower()

        # Find existing hotspot for this city
        existing_hotspot = None

        for hotspot in hotspots:

            if hotspot["city"].lower() == city.lower():

                existing_hotspot = hotspot

                break


        # ======================================
        # DETERMINE CITIZEN REPORT SEVERITY
        # ======================================

        if any(word in description for word in [
            "heavy",
            "thick",
            "severe",
            "strong smoke",
            "large fire"
        ]):

            citizen_risk = "HIGH"

        elif any(word in description for word in [
            "smoke",
            "burning",
            "fire",
            "dust",
            "chemical",
            "gas",
            "industrial",
            "factory"
        ]):

            citizen_risk = "MODERATE"

        else:

            citizen_risk = "LOW"


        # ======================================
        # ADD TO EXISTING HOTSPOT
        # ======================================

        if existing_hotspot:

            existing_hotspot["citizen_reports"] += 1

            existing_hotspot["evidence"].append(
                f"Citizen report: {report['description']}"
            )

            # Increase risk if citizen report is serious
            if citizen_risk == "HIGH":

                existing_hotspot["risk"] = "VERY HIGH"

            elif (
                citizen_risk == "MODERATE"
                and existing_hotspot["risk"] == "LOW"
            ):

                existing_hotspot["risk"] = "MODERATE"


        # ======================================
        # CREATE NEW CITIZEN HOTSPOT
        # ======================================

        else:

            hotspots.append({

                "city": city,

                "latitude": report["latitude"],

                "longitude": report["longitude"],

                "risk": citizen_risk,

                "pm25": None,

                "citizen_reports": 1,

                "evidence": [
                    f"Citizen report: {report['description']}"
                ],

                "source": "Citizen observation",

                "recommended_action": (
                    "Verify the reported location using "
                    "local environmental measurements "
                    "and field inspection."
                )
            })


    # ==========================================
    # PART 3: FINAL INTELLIGENCE
    # ==========================================

    for hotspot in hotspots:

        if (
            hotspot["citizen_reports"] > 0
            and hotspot["pm25"] is not None
        ):

            hotspot["source"] = (
                "Environmental data + Citizen observations"
            )

            hotspot["recommended_action"] = (
                "Prioritize verification of this location "
                "using local air-quality measurements and "
                "field inspection."
            )


    return hotspots