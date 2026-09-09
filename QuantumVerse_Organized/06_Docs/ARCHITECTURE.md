# QuantumVerse — Architecture

## System Overview
```
┌─────────────────────────────────────────────────────────┐
│                    USERS (Browser)                       │
└───────────────┬─────────────────────────────────────────┘
                │ HTTPS
┌───────────────▼─────────────────────────────────────────┐
│              NGINX (Reverse Proxy :80/:443)              │
└───────┬───────────────────────────┬─────────────────────┘
        │ /                         │ /api
┌───────▼──────────┐    ┌──────────▼──────────────────────┐
│  01_Frontend     │    │  02_Backend                      │
│  Next.js :3000   │    │  FastAPI   :8000                 │
│                  │    │                                  │
│  • 18 pages      │    │  • REST API (v1)                 │
│  • App Router    │    │  • Quantum simulator             │
│  • Tailwind CSS  │    │  • AI tutor (OpenAI)             │
│  • Zustand       │◄──►│  • JWT auth                      │
│  • PWA           │    │  • Rate limiting                 │
└──────────────────┘    └──────────┬──────────────────────┘
                                   │
               ┌───────────────────┼─────────────────┐
               │                   │                 │
┌──────────────▼───┐  ┌────────────▼──┐  ┌──────────▼───┐
│  03_Database     │  │  Redis :6379  │  │  OpenAI API  │
│  PostgreSQL:5432 │  │  (cache/sess) │  │  (AI tutor)  │
│  • 12 tables     │  └───────────────┘  └──────────────┘
│  • Alembic ORM   │
└──────────────────┘
```

## Data Flow
1. User opens browser → Next.js frontend served by Nginx
2. Frontend calls `/api/v1/*` → FastAPI backend
3. Backend reads/writes PostgreSQL via SQLAlchemy
4. Quantum simulations run in-process (pure Python statevector)
5. AI tutor calls OpenAI GPT-4 with quantum-specific system prompt
6. Redis caches responses + manages rate limits

## Key Design Decisions
- **Statevector simulation** in pure Python (no Qiskit dependency)
- **JWT authentication** with refresh tokens stored in Redis
- **Supabase-compatible** schema (can swap Supabase for self-hosted PG)
- **PWA** support for offline use of standalone simulator
- **No vendor lock-in** — swap AI provider via `ai/provider.py`
