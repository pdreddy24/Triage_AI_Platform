from core.config.settings import settings


def decide(probability: float) -> str:
    if probability >= settings.BLOCK_THRESHOLD:
        return "BLOCK"
    elif probability >= settings.REVIEW_THRESHOLD:
        return "REVIEW"
    return "APPROVE"