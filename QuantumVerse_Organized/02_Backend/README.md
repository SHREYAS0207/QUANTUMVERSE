# QuantumVerse — Backend

**Stack:** FastAPI · Python 3.11 · SQLAlchemy · Alembic · Pydantic v2 · Redis

## Structure
```
app/
  main.py           — FastAPI entry point
  api/v1/           — REST endpoints
    auth.py         — JWT login / register
    circuits.py     — Save & load circuits
    simulation.py   — Run quantum simulation
    algorithms.py   — Grover, QFT, Deutsch-Jozsa, Teleportation
    ai_tutor.py     — AI tutor chat
    ai_circuit.py   — AI circuit generation
    learning.py     — Lessons & modules
    quiz.py         — Quiz engine
    achievements.py — XP & badge awards
    community.py    — Community posts
    export.py       — Export circuits (QASM, JSON)
    health.py       — Health check
  quantum/
    simulator.py    — Pure-Python statevector simulator
    engine.py       — Gate application engine
    step_executor.py— Step-by-step execution
    error_correction.py — QEC codes
    algorithms/     — Named algorithm implementations
  ai/
    provider.py     — OpenAI / Anthropic wrapper
    prompts.py      — System prompts
  models/           — SQLAlchemy ORM models
  schemas/          — Pydantic request/response schemas
  core/             — Config, security, rate-limit, cache
  database/         — Session, connection, seeder
  services/         — Email service
  data/             — Lesson seed data
tests/
  test_api.py
  test_quantum.py
```

## Quick Start
```bash
pip install -r requirements.txt
cp .env.example .env                # fill in DB_URL, SECRET_KEY, OPENAI_KEY …
alembic upgrade head                # run migrations
uvicorn app.main:app --reload       # http://localhost:8000
```

## Docker
```bash
docker build -t quantumverse-backend .
docker run -p 8000:8000 quantumverse-backend
```

## Key API Routes
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/auth/register | Register |
| POST | /api/v1/auth/login | Login |
| POST | /api/v1/simulation/run | Run simulation |
| GET | /api/v1/circuits | List circuits |
| POST | /api/v1/ai-tutor/chat | AI tutor |
| GET | /api/v1/algorithms | List algorithms |
