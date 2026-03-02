def get_risk_band(score: float):
    if score < 0.3:
        return "LOW"
    elif score < 0.7:
        return "MEDIUM"
    elif score < 0.9:
        return "HIGH"
    else:
        return "CRITICAL"


def get_route(band: str):
    routes = {
        "LOW": "AUTO_APPROVE",
        "MEDIUM": "JUNIOR_QUEUE",
        "HIGH": "SENIOR_QUEUE",
        "CRITICAL": "AUTO_BLOCK"
    }
    return routes.get(band, "REVIEW")