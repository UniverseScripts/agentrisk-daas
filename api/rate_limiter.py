import time
from fastapi import HTTPException, status
import redis.asyncio as redis
from core.config import settings

# Air-gapped Redis configuration via Pydantic Settings
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

# Engineered Asynchronous Lua Script (Sliding Window Algorithm using Sorted Sets)
SLIDING_WINDOW_LUA = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local current_time = tonumber(ARGV[3])

-- Expunge stale timestamps prior to the window border
redis.call('ZREMRANGEBYSCORE', key, 0, current_time - window)

-- Compute existing metrics strictly
local count = redis.call('ZCARD', key)

if count >= limit then
    return 0
else
    -- Add the temporal token and reset the expiry for idempotency mapping
    redis.call('ZADD', key, current_time, current_time)
    redis.call('PEXPIRE', key, window)
    return 1
end
"""

async def enforce_rate_limit(api_key_hash: str, limit: int = 10, window_secs: int = 60):
    """
    Executes the sliding-window token bucket atomic rate limiter using Lua logic over Redis.
    Throws an HTTP 429 if the request threshold overflows the given limit.
    """
    current_time_ms = int(time.time() * 1000)
    
    # eval args: script, numkeys, *keys, *args
    allowed = await redis_client.eval(
        SLIDING_WINDOW_LUA, 
        1, 
        f"ratelimit:sliding:{api_key_hash}", 
        limit,
        window_secs * 1000, 
        current_time_ms
    )
    
    if allowed == 0:
         raise HTTPException(
             status_code=status.HTTP_429_TOO_MANY_REQUESTS,
             detail="Strict Rate Limit Enforced. Throttling applied."
         )
