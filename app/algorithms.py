import time
from app.redis_client import client

def token_bucket(client_id: str, limit: int, window: int) -> dict:
    key = f"token_bucket:{client_id}"
    now = time.time()
    refill_rate = limit / window  # tokens per second

    lua_script = """
    local key = KEYS[1]
    local now = tonumber(ARGV[1])
    local limit = tonumber(ARGV[2])
    local refill_rate = tonumber(ARGV[3])

    local data = redis.call('HMGET', key, 'tokens', 'last_refill')
    local tokens = tonumber(data[1])
    local last_refill = tonumber(data[2])

    if tokens == nil then
        tokens = limit
        last_refill = now
    end

    local elapsed = now - last_refill
    tokens = math.min(limit, tokens + elapsed * refill_rate)

    local allowed = 0
    if tokens >= 1 then
        tokens = tokens - 1
        allowed = 1
    end

    redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
    redis.call('EXPIRE', key, 3600)

    return {allowed, math.floor(tokens)}
    """

    result = client.eval(lua_script, 1, key, now, limit, refill_rate)

    return {
        "allowed": bool(result[0]),
        "remaining": int(result[1]),
        "limit": limit,
        "algorithm": "token_bucket"
    }