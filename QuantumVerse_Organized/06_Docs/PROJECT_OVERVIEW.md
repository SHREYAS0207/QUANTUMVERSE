# QuantumVerse AI 🔬

**AI-Powered Interactive Quantum Algorithm Learning & Simulation Platform**

> Learn quantum computing by building real circuits, running simulations with Qiskit, solving quizzes, and chatting with an AI tutor — all in one platform.

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.12+
- (Optional) OpenRouter API key for full AI features

### 1. Clone & configure
```bash
git clone https://github.com/your-org/quantumverse.git
cd quantumverse

# Backend env
cp backend/.env.example backend/.env
# Edit backend/.env — add your SECRET_KEY and OPENROUTER_API_KEY

# Frontend env
cp frontend/.env.example frontend/.env.local
```

### 2. Run with Docker (recommended)
```bash
docker compose up -d

# Visit:
# Frontend  →  http://localhost:3000
# API docs  →  http://localhost:8000/docs
# Admin     →  http://localhost:3000/admin
```

### 3. Run locally (dev)
```bash
# Terminal 1 — PostgreSQL
docker compose up db -d

# Terminal 2 — Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 3 — Frontend
cd frontend
npm install
npm run dev
```

### 4. Seed database
```bash
cd backend
python seed.py
```

---

## 🏗️ Architecture

```
quantumverse/
├── backend/              # FastAPI + Qiskit + SQLAlchemy
│   ├── app/
│   │   ├── api/v1/       # 8 REST routers
│   │   ├── quantum/      # Qiskit engine + algorithms
│   │   ├── ai/           # OpenRouter AI provider
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── core/         # Config, security, dependencies
│   └── tests/            # Pytest test suites
├── frontend/             # Next.js 14 + TypeScript + Tailwind
│   └── src/
│       ├── app/          # App Router pages
│       ├── components/   # UI, quantum-lab, gamification
│       ├── hooks/        # Data-fetching hooks
│       ├── stores/       # Zustand state
│       └── services/     # API layer
├── nginx/                # Reverse proxy config
├── .github/workflows/    # CI/CD pipelines
└── docker-compose.yml    # Full stack orchestration
```

---

## 🔧 Tech Stack

| Layer        | Technology                              |
|--------------|-----------------------------------------|
| Frontend     | Next.js 14, TypeScript, Tailwind CSS    |
| UI           | Framer Motion, Recharts, Radix UI       |
| State        | Zustand, React Query                    |
| Backend      | FastAPI, Python 3.12, Uvicorn           |
| Quantum      | Qiskit 1.2, Qiskit Aer 0.14            |
| AI           | OpenRouter API (Llama 3.1 8B free)      |
| Database     | PostgreSQL 16, SQLAlchemy async, asyncpg|
| Auth         | JWT (python-jose) + bcrypt              |
| Deploy       | Docker, Nginx, Vercel, Railway          |
| CI/CD        | GitHub Actions                          |

---

## 🌟 Features by Phase

| Phase | Features |
|-------|----------|
| 1 | Project scaffold, models, DB schema |
| 2 | Full backend (40 files), frontend scaffold (44 files) |
| 3 | Quantum Lab UI, AI Tutor chat, Algorithm Explorer, Quiz, Profile |
| 4 | Real Qiskit algorithms, complete REST API, test suite |
| 5 | Rich lesson viewer (KaTeX + syntax highlighting), gamification, leaderboard |
| 6 | Docker, Nginx, GitHub Actions CI/CD, Vercel deploy |
| 7 | Admin dashboard, analytics charts, system health, final polish |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v

# Quantum engine only (no DB needed)
pytest tests/test_quantum.py -v
```

---

## 🚢 Deployment

### Vercel (Frontend)
```bash
npm i -g vercel
cd frontend && vercel --prod
```

### Railway (Backend)
```bash
# Install Railway CLI, then:
railway login && railway up
```

### Docker Production
```bash
docker compose -f docker-compose.yml up -d --build
```

---

## 📝 Environment Variables

See `backend/.env.example` and `frontend/.env.example`.

**Required:**
- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — Random 256-bit key (`openssl rand -hex 32`)

**Optional:**
- `OPENROUTER_API_KEY` — For AI tutor (works without it, uses fallback answers)

---

## 📄 License

MIT — see [LICENSE](LICENSE).
