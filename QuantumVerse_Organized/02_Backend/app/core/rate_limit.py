"""Simple in-memory + Redis rate limiter."""
import time
from collections import defaultdict
from fastapi import Request, HTTPException
from app.core.cache import get, set

_local: dict[str, list[float]] = defaultdict(list)


async def rate_limit(request: Request, limit: int = 60, window: int = 60):
    """Allow `limit` requests per `window` seconds per IP. Use as a FastAPI dependency."""
    ip = request.client.host if request.client else "unknown"
    key = f"rl:{ip}"

    now = time.time()
    hits = _local[key]
    hits[:] = [t for t in hits if t > now - window]

    if len(hits) >= limit:
        raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")

    hits.append(now)


async def simulation_rate_limit(request: Request):
    """Stricter limit for compute-heavy simulation endpoints: 20/min."""
    await rate_limit(request, limit=20, window=60)
