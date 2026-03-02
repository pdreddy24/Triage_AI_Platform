import redis
import logging
from core.config.settings import settings

logger = logging.getLogger(__name__)

# Create Redis client with fast timeouts so Redis downtime doesn't cause delays
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    socket_timeout=0.5,
    socket_connect_timeout=0.5
)


def update_velocity(user_id: str) -> int:
    """
    Increment and return transaction count
    within the configured velocity window.
    Falls back to 0 instantly if Redis is unavailable.
    """
    key = f"velocity:{user_id}"

    try:
        if redis_client.exists(key):
            redis_client.incr(key)
        else:
            redis_client.setex(
                key,
                settings.VELOCITY_WINDOW_SECONDS,
                1
            )

        value = redis_client.get(key)
        return int(value)

    except Exception as e:
        logger.error(f"Redis velocity error: {e}")
        # Fail-safe: return 0 if Redis is down
        return 0