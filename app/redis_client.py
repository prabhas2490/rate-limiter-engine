import redis
import os
# decode_responses=True converts Redis bytes to strings automatically
client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)
