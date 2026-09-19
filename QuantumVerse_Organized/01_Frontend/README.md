# QuantumVerse — Frontend

**Stack:** Next.js 14 · React 18 · TypeScript · Tailwind CSS · Zustand

## Structure
```
src/
  app/          — Next.js App Router pages (15 routes)
  components/   — Reusable UI components
    layout/     — AppShell, Sidebar
    quantum-lab/— Circuit canvas, gate palette, simulation panel
    gamification/— XP bar, streak tracker, level-up modal
    shared/     — Cards, buttons, badges, spinners
    learn/      — Lesson content & sidebar
    ui/         — Low-level primitives
  hooks/        — useAuth, useCircuit, useLearning
  lib/          — API client, Supabase, utils, constants
  services/     — aiService, circuitService, simulationService …
  stores/       — Zustand stores (auth, circuit)
  types/        — TypeScript type definitions
public/         — PWA manifest, service worker
```

## Pages
- `/` Home · `/login` · `/signup` · `/onboarding`
- `/dashboard` · `/learn` · `/quantum-lab` · `/algorithms`
- `/ai-tutor` · `/quiz` · `/achievements` · `/progress`
- `/leaderboard` · `/community` · `/profile` · `/settings`
- `/admin` · `/error-correction`

## Quick Start
```bash
npm install
cp .env.local.example .env.local   # fill in your API URL & Supabase keys
npm run dev                         # http://localhost:3000
```

## Docker
```bash
docker build -t quantumverse-frontend .
docker run -p 3000:3000 quantumverse-frontend
```
