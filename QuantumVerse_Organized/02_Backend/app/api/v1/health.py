"""Health check and metrics endpoints."""
import time
import platform
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="/system", tags=["system"])
_start_time = time.time()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
        "uptime_seconds": round(time.time() - _start_time),
        "python": platform.python_version(),
    }


@router.get("/metrics")
async def metrics():
    """Basic Prometheus-style text metrics."""
    uptime = round(time.time() - _start_time)
    lines = [
        "# HELP quantumverse_uptime_seconds Total uptime in seconds",
        "# TYPE quantumverse_uptime_seconds gauge",
        f"quantumverse_uptime_seconds {uptime}",
        "",
        "# HELP quantumverse_info Version info",
        "# TYPE quantumverse_info gauge",
        f"quantumverse_info{{version=\"{settings.APP_VERSION}\"}} 1",
    ]
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse("\n".join(lines), media_type="text/plain; version=0.0.4")
