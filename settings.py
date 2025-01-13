import os

settings = {
    "API_TOKEN": "my_secure_token",
    "RETRY_COUNT": 3,
    "RETRY_DELAY": 5,  # seconds
    "CACHE_DB_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
}
