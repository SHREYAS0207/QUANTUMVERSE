"""Redis cache abstraction (falls back to in-memory if Redis unavailable)."""
import json
import asyncio
import time
from typing import Any
from app.core.config import settings
import logging

log = logging.getLogger(__name__)

_memory: dict[str, tuple[Any, float]] = {}


try:
    import redis.asyncio as aioredis
    _redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=2)
    _use_redis = True
except Exception:
    _use_redis = False
    log.info("Redis unavailable, using in-memory cache.")


async def get(key: str) -> Any | None:
    if _use_redis:
        try:
            val = await _redis_client.get(key)
            return json.loads(val) if val else None
        except Exception:
            pass
    val, exp = _memory.get(key, (None, 0))
    return val if exp > time.time() else None


async def set(key: str, value: Any, ttl: int = 300) -> None:
    if _use_redis:
        try:
            await _redis_client.setex(key, ttl, json.dumps(value))
            return
        except Exception:
            pass
    _memory[key] = (value, time.time() + ttl)


async def delete(key: str) -> None:
    if _use_redis:
        try:
            await _redis_client.delete(key)
        except Exception:
            pass
    _memory.pop(key, None)


async def cache_simulation(circuit_hash: str, result: dict, ttl: int = 600) -> None:
    await set(f"sim:{circuit_hash}", result, ttl)

async def get_cached_simulation(circuit_hash: str) -> dict | None:
    return await get(f"sim:{circuit_hash}")
