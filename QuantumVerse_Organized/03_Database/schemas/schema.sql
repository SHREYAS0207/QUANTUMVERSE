-- QuantumVerse Database Schema
-- PostgreSQL (via Supabase or self-hosted)

-- ── USERS ────────────────────────────────────────────────────
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT UNIQUE NOT NULL,
    username    TEXT UNIQUE NOT NULL,
    hashed_pw   TEXT NOT NULL,
    display_name TEXT,
    avatar_url  TEXT,
    xp          INTEGER DEFAULT 0,
    level       INTEGER DEFAULT 1,
    streak      INTEGER DEFAULT 0,
    last_active TIMESTAMPTZ DEFAULT NOW(),
    is_active   BOOLEAN DEFAULT TRUE,
    is_admin    BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── CIRCUITS ─────────────────────────────────────────────────
CREATE TABLE circuits (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    description TEXT,
    gates       JSONB NOT NULL DEFAULT '[]',
    num_qubits  INTEGER NOT NULL DEFAULT 2,
    tags        TEXT[] DEFAULT '{}',
    is_public   BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── SIMULATIONS ──────────────────────────────────────────────
CREATE TABLE simulations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    circuit_id      UUID REFERENCES circuits(id) ON DELETE SET NULL,
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    statevector     JSONB,
    probabilities   JSONB,
    measurement     JSONB,
    shots           INTEGER DEFAULT 1024,
    execution_time  FLOAT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ── LEARNING MODULES ─────────────────────────────────────────
CREATE TABLE modules (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT NOT NULL,
    slug        TEXT UNIQUE NOT NULL,
    description TEXT,
    order_index INTEGER DEFAULT 0,
    difficulty  TEXT CHECK(difficulty IN ('beginner','intermediate','advanced')),
    xp_reward   INTEGER DEFAULT 100,
    is_published BOOLEAN DEFAULT TRUE
);

CREATE TABLE lessons (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id   UUID REFERENCES modules(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    content     TEXT,
    order_index INTEGER DEFAULT 0,
    xp_reward   INTEGER DEFAULT 50
);

-- ── USER PROGRESS ────────────────────────────────────────────
CREATE TABLE user_progress (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    module_id   UUID REFERENCES modules(id),
    lesson_id   UUID REFERENCES lessons(id),
    completed   BOOLEAN DEFAULT FALSE,
    score       INTEGER,
    completed_at TIMESTAMPTZ,
    UNIQUE(user_id, lesson_id)
);

-- ── QUIZ ─────────────────────────────────────────────────────
CREATE TABLE quiz_questions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id   UUID REFERENCES modules(id),
    question    TEXT NOT NULL,
    options     JSONB NOT NULL,
    correct_idx INTEGER NOT NULL,
    explanation TEXT,
    difficulty  TEXT DEFAULT 'medium'
);

CREATE TABLE quiz_attempts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    module_id   UUID REFERENCES modules(id),
    score       INTEGER,
    total       INTEGER,
    answers     JSONB,
    xp_earned   INTEGER DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── ACHIEVEMENTS ─────────────────────────────────────────────
CREATE TABLE achievements (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug        TEXT UNIQUE NOT NULL,
    title       TEXT NOT NULL,
    description TEXT,
    icon        TEXT,
    xp_reward   INTEGER DEFAULT 0,
    condition   JSONB
);

CREATE TABLE user_achievements (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id        UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_id UUID REFERENCES achievements(id),
    earned_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);

-- ── AI SESSIONS ──────────────────────────────────────────────
CREATE TABLE ai_sessions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    messages    JSONB DEFAULT '[]',
    topic       TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── COMMUNITY ────────────────────────────────────────────────
CREATE TABLE community_posts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    content     TEXT,
    circuit_id  UUID REFERENCES circuits(id),
    likes       INTEGER DEFAULT 0,
    tags        TEXT[],
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ── INDEXES ──────────────────────────────────────────────────
CREATE INDEX idx_circuits_user    ON circuits(user_id);
CREATE INDEX idx_simulations_user ON simulations(user_id);
CREATE INDEX idx_progress_user    ON user_progress(user_id);
CREATE INDEX idx_attempts_user    ON quiz_attempts(user_id);
CREATE INDEX idx_ua_user          ON user_achievements(user_id);
CREATE INDEX idx_posts_user       ON community_posts(user_id);
