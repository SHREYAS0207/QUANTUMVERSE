from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.core.config import settings
from app.database.connection import engine
from app.models.user import Base as UserBase
from app.models.circuit import Base as CircuitBase
from app.models.learning import Base as LearningBase
from app.models.quiz import Base as QuizBase
from app.models.ai import Base as AIBase
from app.models.achievement import Achievement, UserAchievement
from app.models import qlearn as qlearn_models
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        for base in [UserBase, CircuitBase, LearningBase, QuizBase, AIBase, qlearn_models.Base]:
            await conn.run_sync(base.metadata.create_all)
        await conn.run_sync(_ensure_circuit_columns)
    yield


def _ensure_circuit_columns(conn):
    columns = {column["name"] for column in inspect(conn).get_columns("circuits")}
    if "is_public" not in columns:
        conn.execute(text("ALTER TABLE circuits ADD COLUMN is_public BOOLEAN NOT NULL DEFAULT FALSE"))
    if "like_count" not in columns:
        conn.execute(text("ALTER TABLE circuits ADD COLUMN like_count INTEGER NOT NULL DEFAULT 0"))


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Quantum Algorithm Learning and Simulation Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.app\.github\.dev",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception:
        database_status = "unavailable"

    try:
        from app.quantum.simulator import run_simulation

        run_simulation(1, 1, [{"gate": "H", "targets": [0], "controls": [], "column": 0}], shots=10)
        quantum_status = "available"
    except Exception:
        quantum_status = "unavailable"

    return {
        "status": "ok",
        "database": database_status,
        "quantum_engine": quantum_status,
        "ai": "available" if settings.OPENROUTER_API_KEY and settings.OPENROUTER_API_KEY != "your-openrouter-key-here" else "demo-mode",
        "version": settings.APP_VERSION,
        "app": settings.APP_NAME,
    }
