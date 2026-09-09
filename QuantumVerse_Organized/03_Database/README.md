# QuantumVerse — Database

**Engine:** PostgreSQL 15 (Supabase recommended) + Redis (cache/sessions)

## Structure
```
schemas/          — SQLAlchemy ORM models + raw schema.sql
  user.py         — Users table
  circuit.py      — Circuits + simulations
  learning.py     — Modules + lessons + progress
  quiz.py         — Questions + attempts
  achievement.py  — Badges + user_achievements
  ai.py           — AI session history
  schema.sql      — Raw CREATE TABLE statements
seeds/
  seed.py         — Master seeder (runs all seeds)
  lessons_seed.py — Lesson content seed data
migrations/
  env.py          — Alembic migration environment
  alembic.ini     — Migration config
connection.py     — DB connection factory
session.py        — SQLAlchemy session management
```

## Tables
| Table | Description |
|-------|-------------|
| users | Auth + XP + streak |
| circuits | Saved quantum circuits |
| simulations | Simulation results & statevectors |
| modules | Learning curriculum modules |
| lessons | Individual lesson content |
| user_progress | Per-user lesson completion |
| quiz_questions | Quiz question bank |
| quiz_attempts | Quiz submission history |
| achievements | Achievement definitions |
| user_achievements | Earned badges per user |
| ai_sessions | AI tutor conversation history |
| community_posts | Shared circuits & posts |

## Setup
```bash
# Option A — Supabase (recommended)
# 1. Create project at https://supabase.com
# 2. Paste schemas/schema.sql into the SQL editor
# 3. Copy connection string to backend .env

# Option B — Self-hosted PostgreSQL
psql -U postgres -c 'CREATE DATABASE quantumverse;'
psql -U postgres -d quantumverse -f schemas/schema.sql
python seeds/seed.py

# Option C — Alembic migrations
cd ../02_Backend
alembic upgrade head
python app/database/seed.py
```

## Redis
```bash
docker run -d -p 6379:6379 redis:7-alpine
# Set REDIS_URL=redis://localhost:6379/0 in backend .env
```
