# QuantumVerse — Full Project

A complete quantum computing learning & simulation platform.

## Repository Structure

```
01_Frontend/          Next.js 14 + React + TypeScript + Tailwind
02_Backend/           FastAPI + Python + SQLAlchemy + Quantum Engine
03_Database/          PostgreSQL schema + ORM models + seeds + migrations
04_Standalone_Simulations/  Single-file 3D quantum simulator (no install)
05_DevOps/            Docker Compose + Nginx + GitHub Actions CI/CD
06_Docs/              Architecture, API reference, project overview
07_BuildScripts/      Generator scripts (reference only)
```

## Quick Start

### ⚡ Instant (no install needed)
```
Open: 04_Standalone_Simulations/quantummind_v2.html
Open: 04_Standalone_Simulations/quantumverse_3d.html
```

### 🐳 Full Stack with Docker
```bash
docker compose -f 05_DevOps/docker-compose.yml up
# → Frontend: http://localhost:3000
# → Backend API: http://localhost:8000
# → API Docs: http://localhost:8000/docs
```

### 🛠 Manual Setup
```bash
# 1. Database
psql -f 03_Database/schemas/schema.sql
python 03_Database/seeds/seed.py

# 2. Backend
cd 02_Backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. Frontend
cd 01_Frontend
npm install && npm run dev
```

## Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS, Zustand |
| Backend | FastAPI, Python 3.11, SQLAlchemy, Alembic, Pydantic v2 |
| Database | PostgreSQL 15, Redis 7 |
| Quantum | Custom statevector simulator (pure Python) |
| AI | OpenAI GPT-4 (swappable via provider.py) |
| Auth | JWT (access + refresh tokens) |
| Deploy | Docker, Nginx, GitHub Actions, Vercel (frontend) |
