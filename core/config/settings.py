import os


class Settings:
    
    BLOCK_THRESHOLD = float(os.getenv("BLOCK_THRESHOLD", 0.85))
    REVIEW_THRESHOLD = float(os.getenv("REVIEW_THRESHOLD", 0.60))

    VELOCITY_WINDOW_SECONDS = int(os.getenv("VELOCITY_WINDOW_SECONDS", 3600))

    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


settings = Settings()