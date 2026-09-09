import os

BASE  = "/data/quantumverse"
FRONT = f"{BASE}/frontend"
BACK  = f"{BASE}/backend"

files = {}

# ====================================================================
# PHASE 6 — DOCKER + CI/CD + DEPLOYMENT
# ====================================================================

# --- Root docker-compose ---
files[f"{BASE}/docker-compose.yml"] = '''
version: "3.9"

services:
  # ─── PostgreSQL ───────────────────────────────────────────────
  db:
    image: postgres:16-alpine
    container_name: quantumverse_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
      POSTGRES_DB: ${POSTGRES_DB:-quantumverse}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"],
      interval: 10s
      timeout: 5s
      retries: 5

  # ─── FastAPI Backend ──────────────────────────────────────────
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: quantumverse_backend
    restart: unless-stopped
    env_file: ./backend/.env
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-password}@db:5432/${POSTGRES_DB:-quantumverse}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # ─── Next.js Frontend ────────────────────────────────────────
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: quantumverse_frontend
    restart: unless-stopped
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000/api/v1
    ports:
      - "3000:3000"
    depends_on:
      - backend

  # ─── Nginx Reverse Proxy ─────────────────────────────────────
  nginx:
    image: nginx:alpine
    container_name: quantumverse_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
'''

# --- Backend Dockerfile ---
files[f"{BACK}/Dockerfile"] = '''
FROM python:3.12-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc g++ libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

# --- Frontend Dockerfile ---
files[f"{FRONT}/Dockerfile"] = '''
FROM node:20-alpine AS base
WORKDIR /app

# Install deps
FROM base AS deps
COPY package.json package-lock.json* ./
RUN npm ci

# Build
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production runner
FROM base AS runner
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs && \\
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000

CMD ["node", "server.js"]
'''

# --- Nginx config ---
os.makedirs(f"{BASE}/nginx", exist_ok=True)
files[f"{BASE}/nginx/nginx.conf"] = '''
events { worker_connections 1024; }

http {
  include mime.types;
  default_type application/octet-stream;
  sendfile on;
  keepalive_timeout 65;
  client_max_body_size 20M;

  # Gzip
  gzip on;
  gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

  upstream backend  { server backend:8000; }
  upstream frontend { server frontend:3000; }

  server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
  }

  server {
    listen 443 ssl;
    server_name quantumverse.ai www.quantumverse.ai;

    ssl_certificate     /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # API
    location /api/ {
      proxy_pass http://backend;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_read_timeout 60s;
    }

    # Docs
    location ~ ^/(docs|redoc|openapi.json) {
      proxy_pass http://backend;
      proxy_set_header Host $host;
    }

    # Frontend
    location / {
      proxy_pass http://frontend;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
    }

    # Health check
    location /health {
      proxy_pass http://backend/health;
    }
  }
}
'''

# --- .env.example ---
files[f"{BACK}/.env.example"] = '''
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/quantumverse
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=quantumverse

# Auth — generate with: openssl rand -hex 32
SECRET_KEY=change-me-to-a-random-256-bit-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI (OpenRouter — free tier: https://openrouter.ai)
OPENROUTER_API_KEY=your-openrouter-key-here
AI_MODEL=meta-llama/llama-3.1-8b-instruct:free

# CORS
CORS_ORIGINS=["http://localhost:3000","https://quantumverse.vercel.app"]

# App
DEBUG=false
'''

files[f"{FRONT}/.env.example"] = '''
# Backend URL (without trailing slash)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Optional analytics
NEXT_PUBLIC_POSTHOG_KEY=
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com
'''

# --- GitHub Actions CI/CD ---
os.makedirs(f"{BASE}/.github/workflows", exist_ok=True)
files[f"{BASE}/.github/workflows/ci.yml"] = '''
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # ─── Backend tests ──────────────────────────────────────────
  backend-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: quantumverse_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install backend deps
        working-directory: backend
        run: pip install -r requirements.txt

      - name: Run quantum engine tests
        working-directory: backend
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:testpass@localhost:5432/quantumverse_test
          SECRET_KEY: test-secret-key-for-ci-only
        run: pytest tests/test_quantum.py -v

      - name: Run API tests
        working-directory: backend
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:testpass@localhost:5432/quantumverse_test
          SECRET_KEY: test-secret-key-for-ci-only
        run: pytest tests/test_api.py -v

  # ─── Frontend lint + type-check ─────────────────────────────
  frontend-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node 20
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: frontend/package-lock.json

      - name: Install frontend deps
        working-directory: frontend
        run: npm ci

      - name: Type check
        working-directory: frontend
        run: npm run type-check

      - name: Lint
        working-directory: frontend
        run: npm run lint

      - name: Build
        working-directory: frontend
        env:
          NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1
        run: npm run build

  # ─── Docker build check ─────────────────────────────────────
  docker-build:
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-check]
    steps:
      - uses: actions/checkout@v4

      - name: Build backend image
        run: docker build -t quantumverse-backend:ci ./backend

      - name: Build frontend image
        run: docker build -t quantumverse-frontend:ci ./frontend
'''

files[f"{BASE}/.github/workflows/deploy.yml"] = '''
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ["v*"]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/quantumverse-backend:latest
            ${{ secrets.DOCKER_USERNAME }}/quantumverse-backend:${{ github.sha }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
          vercel-args: "--prod"
'''

# --- Vercel config ---
files[f"{FRONT}/vercel.json"] = '''{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend.railway.app/api/:path*"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options",   "value": "nosniff" },
        { "key": "X-Frame-Options",           "value": "DENY" },
        { "key": "X-XSS-Protection",          "value": "1; mode=block" },
        { "key": "Referrer-Policy",           "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
'''

# ====================================================================
# PHASE 7 — ADMIN DASHBOARD + ANALYTICS + FINAL POLISH
# ====================================================================

# --- Admin dashboard page ---
files[f"{FRONT}/src/app/admin/page.tsx"] = '''
"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Users, Zap, BookOpen, Trophy, TrendingUp, Activity,
  Database, Server, RefreshCw,
} from "lucide-react";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { PageHeader } from "@/components/ui/PageHeader";
import { StatCard } from "@/components/ui/StatCard";

// ── Mock analytics data ──────────────────────────────────────────────
const DAILY_USERS = [
  { date: "Mon", users: 42 }, { date: "Tue", users: 58 },
  { date: "Wed", users: 71 }, { date: "Thu", users: 65 },
  { date: "Fri", users: 89 }, { date: "Sat", users: 54 },
  { date: "Sun", users: 38 },
];

const LEVEL_DIST = [
  { name: "1-5",   value: 45, color: "#00d4ff" },
  { name: "6-10",  value: 28, color: "#a855f7" },
  { name: "11-20", value: 18, color: "#22c55e" },
  { name: "21+",   value:  9, color: "#f59e0b" },
];

const ALGO_RUNS = [
  { name: "Grover",       runs: 1240 },
  { name: "Teleportation",runs:  980 },
  { name: "DJ",           runs:  760 },
  { name: "QFT",          runs:  540 },
];

const CIRCUIT_SAVES = [
  { week: "W1", saves: 120 }, { week: "W2", saves: 184 },
  { week: "W3", saves: 210 }, { week: "W4", saves: 267 },
  { week: "W5", saves: 312 }, { week: "W6", saves: 298 },
];

const TOOLTIP_STYLE = {
  contentStyle: { background: "#0d0d1a", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 12, fontSize: 12 },
  labelStyle:   { color: "#a0a0b0" },
  itemStyle:    { color: "#00d4ff" },
};

export default function AdminPage() {
  const [refreshing, setRefreshing] = useState(false);

  function handleRefresh() {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 1200);
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
      <div className="flex items-center justify-between">
        <PageHeader
          icon={<Server className="w-6 h-6 text-quantum-blue" />}
          title="Admin Dashboard"
          subtitle="Platform analytics and system health"
        />
        <button onClick={handleRefresh}
          className="flex items-center gap-2 text-sm text-muted-foreground hover:text-white transition-colors">
          <RefreshCw className={`w-4 h-4 ${refreshing ? "animate-spin text-quantum-blue" : ""}`} />
          Refresh
        </button>
      </div>

      {/* KPI row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { icon: Users,    label: "Total Users",      value: "2,847",  delta: "+14%",  up: true  },
          { icon: Zap,      label: "Total XP Awarded", value: "1.2M",   delta: "+23%",  up: true  },
          { icon: BookOpen, label: "Lessons Completed",value: "18,420", delta: "+8%",   up: true  },
          { icon: Trophy,   label: "Quiz Attempts",    value: "9,104",  delta: "-3%",   up: false },
        ].map((stat, i) => (
          <motion.div key={stat.label} initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
            transition={{ delay: i * 0.08 }}
            className="glass rounded-xl border border-white/5 p-5">
            <div className="flex items-center justify-between mb-3">
              <stat.icon className="w-5 h-5 text-quantum-blue" />
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                stat.up ? "text-green-400 bg-green-400/10" : "text-red-400 bg-red-400/10"
              }`}>{stat.delta}</span>
            </div>
            <p className="text-2xl font-bold text-white">{stat.value}</p>
            <p className="text-xs text-muted-foreground mt-1">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      {/* Charts row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* DAU */}
        <div className="lg:col-span-2 glass rounded-xl border border-white/5 p-6">
          <h3 className="text-sm font-semibold text-white mb-5">Daily Active Users (7d)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={DAILY_USERS}>
              <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <Tooltip {...TOOLTIP_STYLE} />
              <Bar dataKey="users" fill="#00d4ff" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Level distribution */}
        <div className="glass rounded-xl border border-white/5 p-6">
          <h3 className="text-sm font-semibold text-white mb-5">User Level Distribution</h3>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie data={LEVEL_DIST} cx="50%" cy="50%" innerRadius={45} outerRadius={70}
                paddingAngle={4} dataKey="value">
                {LEVEL_DIST.map((entry, i) => <Cell key={i} fill={entry.color} />)}
              </Pie>
              <Tooltip {...TOOLTIP_STYLE} formatter={(v: any) => [`${v}%`, "Users"]} />
            </PieChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-2 gap-2 mt-3">
            {LEVEL_DIST.map(d => (
              <div key={d.name} className="flex items-center gap-1.5">
                <div className="w-2 h-2 rounded-full" style={{ background: d.color }} />
                <span className="text-xs text-muted-foreground">Lvl {d.name}</span>
                <span className="text-xs text-white ml-auto">{d.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Charts row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Algorithm popularity */}
        <div className="glass rounded-xl border border-white/5 p-6">
          <h3 className="text-sm font-semibold text-white mb-5">Algorithm Runs (All Time)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={ALGO_RUNS} layout="vertical">
              <XAxis type="number" tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <YAxis dataKey="name" type="category" tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} width={90} />
              <Tooltip {...TOOLTIP_STYLE} />
              <Bar dataKey="runs" fill="#a855f7" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Circuit saves trend */}
        <div className="glass rounded-xl border border-white/5 p-6">
          <h3 className="text-sm font-semibold text-white mb-5">Circuit Saves (6 Weeks)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={CIRCUIT_SAVES}>
              <XAxis dataKey="week" tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <Tooltip {...TOOLTIP_STYLE} />
              <Line type="monotone" dataKey="saves" stroke="#22c55e" strokeWidth={2}
                dot={{ fill: "#22c55e", r: 4 }} activeDot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* System health */}
      <div className="glass rounded-xl border border-white/5 p-6">
        <h3 className="text-sm font-semibold text-white mb-5 flex items-center gap-2">
          <Activity className="w-4 h-4 text-quantum-blue" />
          System Health
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "API Latency",      value: "48ms",    status: "ok"   },
            { label: "DB Connections",   value: "12 / 100", status: "ok"  },
            { label: "Qiskit Jobs/min",  value: "340",     status: "ok"   },
            { label: "Error Rate",       value: "0.12%",   status: "warn" },
          ].map(item => (
            <div key={item.label} className="p-4 rounded-xl bg-white/3 border border-white/5">
              <div className="flex items-center gap-2 mb-2">
                <div className={`w-2 h-2 rounded-full ${
                  item.status === "ok" ? "bg-green-400" : "bg-yellow-400"
                }`} />
                <p className="text-xs text-muted-foreground">{item.label}</p>
              </div>
              <p className="text-lg font-bold text-white">{item.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
'''

# --- Complete final README ---
files[f"{BASE}/README.md"] = '''
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
'''

# --- LICENSE ---
files[f"{BASE}/LICENSE"] = '''
MIT License

Copyright (c) 2026 QuantumVerse AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# --- .gitignore ---
files[f"{BASE}/.gitignore"] = '''
# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/
*.egg-info/
dist/
build/
.pytest_cache/

# Node
node_modules/
.next/
out/
.vercel/

# Env files
.env
.env.local
.env.production
.env.production.local
!.env.example

# Docker
nginx/ssl/

# OS
.DS_Store
Thumbs.db
*.swp
*.swo

# IDE
.vscode/
.idea/
*.code-workspace

# Logs
*.log
logs/
'''

# --- Makefile for convenience ---
files[f"{BASE}/Makefile"] = '''
.PHONY: dev build test seed clean

# Development
dev:
\tdocker compose up db -d
\t@echo "Starting backend..."
\tcd backend && uvicorn app.main:app --reload &
\t@echo "Starting frontend..."
\tcd frontend && npm run dev

# Docker full stack
build:
\tdocker compose up --build -d

# Seed the database
seed:
\tcd backend && python seed.py

# Run tests
test:
\tcd backend && pytest tests/ -v

# Stop everything
stop:
\tdocker compose down

# Clean volumes
clean:
\tdocker compose down -v --remove-orphans

# Check backend health
health:
\tcurl -s http://localhost:8000/health | python3 -m json.tool

# View logs
logs:
\tdocker compose logs -f backend
'''

# --- Final Sidebar component update with admin link ---
files[f"{FRONT}/src/components/ui/Sidebar.tsx"] = '''
"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  Atom, BookOpen, BrainCircuit, Home, Trophy,
  Settings, User, Cpu, HelpCircle, LayoutDashboard,
  FlaskConical, Medal,
} from "lucide-react";

const NAV = [
  { label: "Dashboard",   href: "/dashboard",   icon: Home         },
  { label: "Quantum Lab", href: "/quantum-lab",  icon: FlaskConical },
  { label: "Learn",       href: "/learn",        icon: BookOpen     },
  { label: "Algorithms",  href: "/algorithms",   icon: Cpu          },
  { label: "AI Tutor",    href: "/ai-tutor",     icon: BrainCircuit },
  { label: "Quiz",        href: "/quiz",         icon: HelpCircle   },
] as const;

const SECONDARY = [
  { label: "Progress",      href: "/progress",     icon: LayoutDashboard },
  { label: "Achievements",  href: "/achievements", icon: Trophy          },
  { label: "Leaderboard",   href: "/leaderboard",  icon: Medal           },
  { label: "Profile",       href: "/profile",      icon: User            },
  { label: "Settings",      href: "/settings",     icon: Settings        },
] as const;

export function Sidebar() {
  const path = usePathname();

  function NavItem({ href, icon: Icon, label }: { href: string; icon: any; label: string }) {
    const active = path === href || (href !== "/dashboard" && path.startsWith(href));
    return (
      <Link href={href}
        className={cn(
          "flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all",
          active
            ? "bg-quantum-blue/10 text-quantum-blue border border-quantum-blue/20"
            : "text-muted-foreground hover:text-white hover:bg-white/5",
        )}
      >
        <Icon className="w-4 h-4 flex-shrink-0" />
        {label}
      </Link>
    );
  }

  return (
    <aside className="w-60 flex-shrink-0 h-screen glass border-r border-white/5 flex flex-col">
      {/* Logo */}
      <div className="p-5 flex items-center gap-2.5 border-b border-white/5">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center">
          <Atom className="w-4 h-4 text-quantum-dark" />
        </div>
        <span className="font-bold text-white text-sm">QuantumVerse</span>
      </div>

      {/* Main nav */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {NAV.map(item => <NavItem key={item.href} {...item} />)}

        <div className="pt-4 pb-2">
          <p className="px-3 text-[10px] font-semibold text-muted-foreground/50 uppercase tracking-wider mb-1">Personal</p>
        </div>
        {SECONDARY.map(item => <NavItem key={item.href} {...item} />)}
      </nav>

      {/* Admin link */}
      <div className="p-3 border-t border-white/5">
        <NavItem href="/admin" icon={LayoutDashboard} label="Admin" />
      </div>
    </aside>
  );
}
'''

# --- next.config.ts update ---
files[f"{FRONT}/next.config.ts"] = '''
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",           // Needed for Docker
  poweredByHeader: false,
  images: {
    domains: ["avatars.githubusercontent.com", "lh3.googleusercontent.com"],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1",
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options",         value: "DENY"                          },
          { key: "X-Content-Type-Options",   value: "nosniff"                       },
          { key: "Referrer-Policy",          value: "strict-origin-when-cross-origin" },
        ],
      },
    ];
  },
};

export default nextConfig;
'''

# ─── Write all files ──────────────────────────────────────────────────
written = 0
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.lstrip('\n'))
    rel = path.replace('/data/quantumverse/', '')
    category = 'FE' if 'frontend' in path else 'BE' if 'backend' in path else 'ROOT'
    print(f"  {category}: {rel}")
    written += 1

print(f"\nPhase 6+7 total: {written} files")
