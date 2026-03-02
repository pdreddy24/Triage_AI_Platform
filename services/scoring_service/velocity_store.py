import redis
from core.config.settings import settings


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


def update_velocity(user_id: str) -> int:
    """
    Increment and return the number of transactions
    for a user within the velocity window.
    """
    key = f"velocity:{user_id}"

    if redis_client.exists(key):
        redis_client.incr(key)
    else:
        redis_client.setex(key, settings.VELOCITY_WINDOW_SECONDS, 1)

    return int(redis_client.get(key))