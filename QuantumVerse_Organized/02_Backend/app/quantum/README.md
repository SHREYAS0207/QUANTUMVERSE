# QLearn Three Flagship Features

Drop-in module pack adding only:
1. QLearn AI Tutor
2. Quantum Problem Solver
3. Quantum Explorer

Includes frontend pages/components, FastAPI backend routers/services, SQLAlchemy models, database migration SQL, tests, and integration notes.

## Install
Copy folders into your existing QuantumVerse project:
- `frontend/src/app/*` -> `01_Frontend/src/app/`
- `frontend/src/components/qlearn` -> `01_Frontend/src/components/qlearn`
- `frontend/src/services/qlearnService.ts` -> `01_Frontend/src/services/`
- `frontend/src/types/qlearn.ts` -> `01_Frontend/src/types/`
- `backend/app/*` -> `02_Backend/app/`
- `database/001_qlearn_three_features.sql` -> run as migration

Register backend router:
```python
from app.api.v1.qlearn import router as qlearn_router
api_router.include_router(qlearn_router, prefix="/qlearn", tags=["qlearn"])
```

Routes exposed:
- `/ai-tutor`
- `/quantum-solver`
- `/quantum-explorer`

API exposed:
- `POST /api/v1/qlearn/ai/chat`
- `POST /api/v1/qlearn/solver/question`
- `POST /api/v1/qlearn/solver/circuit`
- `POST /api/v1/qlearn/solver/verify`
- `POST /api/v1/qlearn/explorer/search`
- `POST /api/v1/qlearn/explorer/simulate`
- `GET /api/v1/qlearn/explorer/videos`
- `GET /api/v1/qlearn/simulations`
- `GET /api/v1/qlearn/user/progress`
