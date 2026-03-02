from core.config.settings import settings


def make_decision(probability: float) -> str:
    if probability >= settings.BLOCK_THRESHOLD:
        return "BLOCK"
    elif probability >= settings.REVIEW_THRESHOLD:
        return "REVIEW"
    else:
        return "APPROVE"