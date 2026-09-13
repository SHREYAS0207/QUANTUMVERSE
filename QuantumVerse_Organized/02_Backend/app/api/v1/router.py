from fastapi import APIRouter
from .auth import router as auth_router
from .circuits import router as circuits_router
from .simulation import router as simulation_router
from .algorithms import router as algorithms_router
from .learning import router as learning_router
from .ai_tutor import router as ai_router
from .quiz import router as quiz_router
from .achievements import router as achievements_router
from .community import router as community_router
from .ai_circuit import router as ai_circuit_router
from .export import router as export_router
from .health import router as system_router
from .qlearn import router as qlearn_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(circuits_router)
api_router.include_router(simulation_router)
api_router.include_router(algorithms_router)
api_router.include_router(learning_router)
api_router.include_router(ai_router)
api_router.include_router(quiz_router)
api_router.include_router(achievements_router)
api_router.include_router(community_router)
api_router.include_router(ai_circuit_router)
api_router.include_router(export_router)
api_router.include_router(system_router)
api_router.include_router(qlearn_router, prefix="/qlearn", tags=["qlearn"])
