from services.climate import get_air_quality


# Temporary storage.
# Later we will replace this with a database.
CITIZEN_REPORTS = []


def add_citizen_report(report):
    """
    Store a citizen pollution report.
    """

    CITIZEN_REPORTS.append(report)

    return report


def get_citizen_reports():
    """
    Return all citizen pollution reports.
    """

    return CITIZEN_REPORTS


def determine_report_risk(description):
    """
    Estimate risk from the citizen's description.
    This is a prototype rule-based signal.
    """

    description = description.lower()

    if any(word in description for word in [
        "heavy",
        "thick",
        "severe",
        "large fire",
        "strong smoke"
    ]):
        return "HIGH"

    if any(word in description for word in [
        "smoke",
        "burning",
        "fire",
        "dust",
        "chemical",
        "gas",
        "industrial",
        "factory"
    ]):
        return "MODERATE"

    return "LOW"


def calculate_hotspot_intelligence():
    """
    Combine environmental data and citizen observations
    to identify potential pollution hotspots.
    """

    hotspots = []

    cities = [
        "Delhi",
        "Mumbai",
        "Kolkata",
        "Bengaluru",
        "Hyderabad"
    ]

    # ==========================================
    # ENVIRONMENTAL SIGNALS
    # ==========================================

    for city in cities:

        air_data = get_air_quality(city)

        if air_data is None:
            continue

        pm25 = air_data["pm25"]

        if pm25 >= 75:
            environmental_risk = "VERY HIGH"

        elif pm25 >= 50:
            environmental_risk = "HIGH"

        elif pm25 >= 35:
            environmental_risk = "MODERATE"

        else:
            environmental_risk = "LOW"

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
    # CITIZEN SIGNALS
    # ==========================================

    for report in CITIZEN_REPORTS:

        city = report["city"]

        description = report["description"]

        citizen_risk = determine_report_risk(
            description
        )

        existing_hotspot = None

        for hotspot in hotspots:

            if hotspot["city"].lower() == city.lower():

                existing_hotspot = hotspot

                break

        # ======================================
        # EXISTING ENVIRONMENTAL HOTSPOT
        # ======================================

        if existing_hotspot:

            existing_hotspot["citizen_reports"] += 1

            # Use the citizen location
            # if this is the first citizen report.
            if existing_hotspot["latitude"] is None:

                existing_hotspot["latitude"] = report[
                    "latitude"
                ]

                existing_hotspot["longitude"] = report[
                    "longitude"
                ]

            existing_hotspot["evidence"].append(
                f"Citizen report: {description}"
            )

            if citizen_risk == "HIGH":

                existing_hotspot["risk"] = "VERY HIGH"

            elif (
                citizen_risk == "MODERATE"
                and existing_hotspot["risk"] == "LOW"
            ):

                existing_hotspot["risk"] = "MODERATE"

            existing_hotspot["source"] = (
                "Environmental data + Citizen observations"
            )

            existing_hotspot["recommended_action"] = (
                "Prioritize verification of this location "
                "using local air-quality measurements and "
                "field inspection."
            )

        # ======================================
        # NEW CITIZEN HOTSPOT
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
                    f"Citizen report: {description}"
                ],

                "source": "Citizen observation",

                "recommended_action": (
                    "Verify the reported location using "
                    "local air-quality measurements and "
                    "field inspection."
                )
            })

    return hotspots


def get_map_hotspots():
    """
    Return geographic hotspot points designed
    for direct frontend map visualization.
    """

    map_points = []

    for report in CITIZEN_REPORTS:

        risk = determine_report_risk(
            report["description"]
        )

        map_points.append({

            "city": report["city"],

            "latitude": report["latitude"],

            "longitude": report["longitude"],

            "risk": risk,

            "description": report["description"],

            "source": "Citizen observation"

        })

    return map_points