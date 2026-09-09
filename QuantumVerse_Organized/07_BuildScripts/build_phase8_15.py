import os

BASE  = "/data/quantumverse"
FRONT = f"{BASE}/frontend"
BACK  = f"{BASE}/backend"

files = {}

# ====================================================================
# PHASE 8 — ONBOARDING WIZARD + EMAIL NOTIFICATIONS
# ====================================================================

files[f"{BACK}/app/services/email.py"] = '''
"""Email service using SMTP (works with Gmail / SendGrid / Mailgun)."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

log = logging.getLogger(__name__)


EMAIL_TEMPLATES = {
    "welcome": {
        "subject": "Welcome to QuantumVerse AI 🔬",
        "body": """
        <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#080812;color:#fff;padding:32px;border-radius:16px">
          <div style="text-align:center;margin-bottom:32px">
            <h1 style="color:#00d4ff;font-size:28px;margin:0">QuantumVerse AI</h1>
            <p style="color:#6b6b80;margin:4px 0">Quantum Computing Mastery Platform</p>
          </div>
          <h2 style="color:#fff">Welcome, {name}! 🎉</h2>
          <p style="color:#a0a0b0;line-height:1.6">You\'re now part of the QuantumVerse community. Your quantum journey starts here.</p>
          <div style="background:#0d0d1a;border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:20px;margin:24px 0">
            <p style="color:#fff;margin:0 0 12px 0;font-weight:600">Get started:</p>
            <ul style="color:#a0a0b0;line-height:2;padding-left:20px">
              <li>Build your first quantum circuit in the <b style="color:#00d4ff">Quantum Lab</b></li>
              <li>Chat with <b style="color:#00d4ff">QubitAI</b> — your AI tutor</li>
              <li>Explore <b style="color:#00d4ff">Grover\'s Algorithm</b> in the Algorithm Explorer</li>
            </ul>
          </div>
          <div style="text-align:center">
            <a href="{app_url}" style="display:inline-block;background:#00d4ff;color:#080812;font-weight:700;padding:12px 32px;border-radius:8px;text-decoration:none">Open QuantumVerse</a>
          </div>
          <p style="color:#4a4a5a;font-size:12px;margin-top:32px;text-align:center">You\'re receiving this because you signed up at quantumverse.ai</p>
        </div>
        """,
    },
    "streak_reminder": {
        "subject": "Don\'t break your streak! 🔥 {streak} days strong",
        "body": """
        <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#080812;color:#fff;padding:32px;border-radius:16px">
          <h2 style="color:#f97316">🔥 {name}, keep your {streak}-day streak alive!</h2>
          <p style="color:#a0a0b0">You\'ve been on a roll. Complete just one lesson or quiz today to keep going!</p>
          <div style="text-align:center;margin-top:24px">
            <a href="{app_url}/learn" style="display:inline-block;background:#f97316;color:#fff;font-weight:700;padding:12px 32px;border-radius:8px;text-decoration:none">Continue Learning</a>
          </div>
        </div>
        """,
    },
    "level_up": {
        "subject": "🎉 Congratulations! You reached Level {level} on QuantumVerse",
        "body": """
        <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#080812;color:#fff;padding:32px;border-radius:16px">
          <div style="text-align:center;margin-bottom:24px">
            <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#a855f7);display:inline-flex;align-items:center;justify-content:center;font-size:36px;font-weight:900;color:#080812">{level}</div>
          </div>
          <h2 style="color:#00d4ff;text-align:center">Level {level} Unlocked!</h2>
          <p style="color:#a0a0b0;text-align:center">{name}, you\'ve reached Level {level} with {xp} XP. Keep pushing!</p>
          <div style="text-align:center;margin-top:24px">
            <a href="{app_url}/profile" style="display:inline-block;background:#00d4ff;color:#080812;font-weight:700;padding:12px 32px;border-radius:8px;text-decoration:none">View Profile</a>
          </div>
        </div>
        """,
    },
}


async def send_email(to: str, template: str, variables: dict) -> bool:
    """Send a templated HTML email."""
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        log.info(f"Email skipped (SMTP not configured): {template} -> {to}")
        return False
    tpl = EMAIL_TEMPLATES.get(template)
    if not tpl:
        return False
    app_url = getattr(settings, "APP_URL", "https://quantumverse.ai")
    body = tpl["body"].format(app_url=app_url, **variables)
    subject = tpl["subject"].format(**variables)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = settings.SMTP_FROM
    msg["To"]      = to
    msg.attach(MIMEText(body, "html"))
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
            s.starttls()
            s.login(settings.SMTP_USER, settings.SMTP_PASS)
            s.sendmail(settings.SMTP_FROM, [to], msg.as_string())
        return True
    except Exception as exc:
        log.error(f"Email send failed: {exc}")
        return False


async def send_welcome(email: str, name: str) -> bool:
    return await send_email(email, "welcome", {"name": name})

async def send_level_up(email: str, name: str, level: int, xp: int) -> bool:
    return await send_email(email, "level_up", {"name": name, "level": level, "xp": xp})

async def send_streak_reminder(email: str, name: str, streak: int) -> bool:
    return await send_email(email, "streak_reminder", {"name": name, "streak": streak})
'''

files[f"{FRONT}/src/app/onboarding/page.tsx"] = '''
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Atom, BookOpen, BrainCircuit, FlaskConical, ArrowRight, Check } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";
import { useAuthStore } from "@/stores/authStore";
import { api } from "@/lib/api";

const LEVELS = [
  { id: "beginner",     label: "Beginner",     desc: "New to quantum computing",       icon: "\ud83c\udf31" },
  { id: "intermediate", label: "Intermediate",  desc: "Know linear algebra & some QM",   icon: "\u26a1" },
  { id: "advanced",     label: "Advanced",      desc: "Research / industry background",  icon: "\ud83d\udd2c" },
];

const GOALS = [
  { id: "learn_basics",    label: "Learn the basics",       icon: BookOpen      },
  { id: "build_circuits",  label: "Build quantum circuits",  icon: FlaskConical  },
  { id: "explore_ai",      label: "Explore AI + quantum",    icon: BrainCircuit  },
  { id: "research",        label: "Research & algorithms",   icon: Atom          },
];

const STEPS = ["Welcome", "Your Level", "Your Goals", "Ready!"];

export default function OnboardingPage() {
  const router   = useRouter();
  const { user, setUser } = useAuthStore();
  const [step,  setStep]  = useState(0);
  const [level, setLevel] = useState("");
  const [goals, setGoals] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);

  function toggleGoal(id: string) {
    setGoals(prev => prev.includes(id) ? prev.filter(g => g !== id) : [...prev, id]);
  }

  async function finish() {
    setSaving(true);
    try {
      await api.put("/auth/profile", { learning_level: level });
    } catch {}
    setSaving(false);
    router.push("/dashboard");
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 bg-quantum-dark">
      {/* Glow */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-quantum-blue/5 blur-3xl" />
      </div>

      {/* Step indicators */}
      <div className="flex gap-2 mb-10">
        {STEPS.map((s, i) => (
          <div key={s} className={`flex items-center gap-2 ${ i < STEPS.length - 1 ? "" : "" }`}>
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
              i < step  ? "bg-quantum-blue text-quantum-dark" :
              i === step ? "border-2 border-quantum-blue text-quantum-blue" :
                           "border border-white/10 text-muted-foreground"
            }`}>
              {i < step ? <Check className="w-3.5 h-3.5" /> : i + 1}
            </div>
            {i < STEPS.length - 1 && <div className={`w-10 h-px ${ i < step ? "bg-quantum-blue" : "bg-white/10" }`} />}
          </div>
        ))}
      </div>

      {/* Card */}
      <AnimatePresence mode="wait">
        <motion.div key={step}
          initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -40 }}
          transition={{ duration: 0.3 }}
          className="w-full max-w-md glass rounded-2xl border border-white/10 p-8">

          {step === 0 && (
            <div className="text-center">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center mx-auto mb-6">
                <Atom className="w-8 h-8 text-quantum-dark" />
              </div>
              <h1 className="text-2xl font-bold text-white mb-2">Welcome to QuantumVerse{user?.name ? `, ${user.name}` : ""}!</h1>
              <p className="text-muted-foreground text-sm mb-8">Let\'s personalise your quantum learning journey in 60 seconds.</p>
              <GlowButton onClick={() => setStep(1)} className="w-full justify-center">
                Let\'s Go <ArrowRight className="w-4 h-4" />
              </GlowButton>
            </div>
          )}

          {step === 1 && (
            <div>
              <h2 className="text-xl font-bold text-white mb-1">What\'s your level?</h2>
              <p className="text-muted-foreground text-sm mb-6">We\'ll tailor explanations and content to match.</p>
              <div className="space-y-3 mb-8">
                {LEVELS.map(l => (
                  <button key={l.id} onClick={() => setLevel(l.id)}
                    className={`w-full text-left p-4 rounded-xl border transition-all ${
                      level === l.id
                        ? "border-quantum-blue bg-quantum-blue/10 text-white"
                        : "border-white/5 bg-white/2 text-muted-foreground hover:border-white/20"
                    }`}>
                    <span className="text-xl mr-3">{l.icon}</span>
                    <span className="font-medium">{l.label}</span>
                    <span className="text-xs block pl-8 mt-0.5 opacity-70">{l.desc}</span>
                  </button>
                ))}
              </div>
              <GlowButton onClick={() => setStep(2)} disabled={!level} className="w-full justify-center">
                Continue <ArrowRight className="w-4 h-4" />
              </GlowButton>
            </div>
          )}

          {step === 2 && (
            <div>
              <h2 className="text-xl font-bold text-white mb-1">What are your goals?</h2>
              <p className="text-muted-foreground text-sm mb-6">Pick all that apply. We\'ll highlight the most relevant content.</p>
              <div className="grid grid-cols-2 gap-3 mb-8">
                {GOALS.map(g => {
                  const active = goals.includes(g.id);
                  return (
                    <button key={g.id} onClick={() => toggleGoal(g.id)}
                      className={`p-4 rounded-xl border transition-all flex flex-col items-center gap-2 ${
                        active ? "border-quantum-blue bg-quantum-blue/10" : "border-white/5 hover:border-white/20"
                      }`}>
                      <g.icon className={`w-5 h-5 ${ active ? "text-quantum-blue" : "text-muted-foreground" }`} />
                      <span className={`text-xs font-medium text-center ${ active ? "text-white" : "text-muted-foreground" }`}>
                        {g.label}
                      </span>
                    </button>
                  );
                })}
              </div>
              <GlowButton onClick={() => setStep(3)} disabled={goals.length === 0} className="w-full justify-center">
                Continue <ArrowRight className="w-4 h-4" />
              </GlowButton>
            </div>
          )}

          {step === 3 && (
            <div className="text-center">
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-2xl font-bold text-white mb-2">You\'re all set!</h2>
              <p className="text-muted-foreground text-sm mb-2">
                Level: <span className="text-quantum-blue font-medium capitalize">{level}</span>
              </p>
              <p className="text-muted-foreground text-sm mb-8">
                {goals.length} goal{goals.length > 1 ? "s" : ""} selected
              </p>
              <GlowButton onClick={finish} loading={saving} className="w-full justify-center">
                Enter QuantumVerse 🚀
              </GlowButton>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
'''

# ====================================================================
# PHASE 9 — CIRCUIT SHARING + COMMUNITY GALLERY
# ====================================================================

files[f"{BACK}/app/api/v1/community.py"] = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.circuit import Circuit, CircuitLike

router = APIRouter(prefix="/community", tags=["community"])


@router.get("/circuits")
async def list_public(db: AsyncSession = Depends(get_db), sort: str = "recent", limit: int = 20):
    """List publicly shared circuits."""
    query = select(Circuit).where(Circuit.is_public == True)
    if sort == "popular":
        query = query.order_by(desc(Circuit.like_count))
    else:
        query = query.order_by(desc(Circuit.created_at))
    rows = await db.execute(query.limit(limit))
    return {"circuits": [_public_dict(c) for c in rows.scalars().all()]}


@router.post("/circuits/{circuit_id}/like")
async def like_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = await _get_public_or_404(db, circuit_id)
    existing = await db.execute(select(CircuitLike).where(CircuitLike.circuit_id == circuit_id, CircuitLike.user_id == user.id))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Already liked")
    db.add(CircuitLike(circuit_id=circuit_id, user_id=user.id))
    c.like_count = (c.like_count or 0) + 1
    await db.commit()
    return {"likes": c.like_count}


@router.delete("/circuits/{circuit_id}/like", status_code=204)
async def unlike_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    existing = await db.execute(select(CircuitLike).where(CircuitLike.circuit_id == circuit_id, CircuitLike.user_id == user.id))
    like = existing.scalar_one_or_none()
    if not like:
        raise HTTPException(404, "Not liked")
    c = await _get_public_or_404(db, circuit_id)
    await db.delete(like)
    c.like_count = max(0, (c.like_count or 1) - 1)
    await db.commit()


@router.post("/circuits/{circuit_id}/publish")
async def publish_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = await _get_owned_or_404(db, circuit_id, user.id)
    c.is_public = True
    await db.commit()
    return {"published": True, "id": str(c.id)}


async def _get_public_or_404(db: AsyncSession, circuit_id: str) -> Circuit:
    row = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.is_public == True))
    c = row.scalar_one_or_none()
    if not c:
        raise HTTPException(404, "Circuit not found")
    return c

async def _get_owned_or_404(db: AsyncSession, circuit_id: str, user_id) -> Circuit:
    row = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.user_id == user_id))
    c = row.scalar_one_or_none()
    if not c:
        raise HTTPException(404, "Circuit not found")
    return c

def _public_dict(c: Circuit) -> dict:
    return {
        "id": str(c.id), "name": c.name, "description": c.description,
        "qubits": c.qubits, "like_count": c.like_count or 0,
        "created_at": c.created_at.isoformat(),
    }
'''

files[f"{FRONT}/src/app/community/page.tsx"] = '''
"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Heart, Share2, FlaskConical, Users } from "lucide-react";
import { PageHeader } from "@/components/ui/PageHeader";
import { api } from "@/lib/api";

interface PublicCircuit {
  id: string; name: string; description: string;
  qubits: number; like_count: number; created_at: string;
}

const SORT_OPTS = ["Recent", "Popular"] as const;

export default function CommunityPage() {
  const [circuits, setCircuits] = useState<PublicCircuit[]>([]);
  const [sort, setSort]     = useState<"Recent" | "Popular">("Recent");
  const [liked, setLiked]   = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.get(`/community/circuits?sort=${sort.toLowerCase()}`)
      .then(r => r.json()).then(d => setCircuits(d.circuits ?? []))
      .finally(() => setLoading(false));
  }, [sort]);

  async function toggleLike(id: string) {
    if (liked.has(id)) {
      await api.delete(`/community/circuits/${id}/like`);
      setLiked(p => { const n = new Set(p); n.delete(id); return n; });
      setCircuits(cs => cs.map(c => c.id === id ? { ...c, like_count: c.like_count - 1 } : c));
    } else {
      await api.post(`/community/circuits/${id}/like`);
      setLiked(p => new Set([...p, id]));
      setCircuits(cs => cs.map(c => c.id === id ? { ...c, like_count: c.like_count + 1 } : c));
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-8">
        <PageHeader icon={<Users className="w-6 h-6 text-quantum-blue" />}
          title="Community Circuits" subtitle="Explore and remix circuits shared by the community" />
        <div className="flex gap-1 p-1 glass rounded-xl border border-white/5">
          {SORT_OPTS.map(o => (
            <button key={o} onClick={() => setSort(o)}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
                sort === o ? "bg-quantum-blue/10 text-quantum-blue border border-quantum-blue/20" : "text-muted-foreground hover:text-white"
              }`}>{o}</button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-44 glass rounded-xl border border-white/5 animate-pulse" />
          ))}
        </div>
      ) : circuits.length === 0 ? (
        <div className="text-center py-20 text-muted-foreground">
          <FlaskConical className="w-12 h-12 mx-auto mb-4 opacity-20" />
          <p>No circuits shared yet. Be the first!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {circuits.map((c, i) => (
            <motion.div key={c.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="glass rounded-xl border border-white/5 p-5 flex flex-col hover:border-quantum-blue/20 transition-all">
              <div className="flex items-start justify-between mb-3">
                <FlaskConical className="w-5 h-5 text-quantum-blue" />
                <span className="text-xs text-muted-foreground">{c.qubits}q</span>
              </div>
              <h3 className="font-semibold text-white text-sm mb-1 truncate">{c.name}</h3>
              <p className="text-xs text-muted-foreground line-clamp-2 flex-1">{c.description || "No description"}</p>
              <div className="flex items-center justify-between mt-4">
                <button onClick={() => toggleLike(c.id)}
                  className={`flex items-center gap-1.5 text-xs transition-colors ${ liked.has(c.id) ? "text-red-400" : "text-muted-foreground hover:text-red-400" }`}>
                  <Heart className={`w-3.5 h-3.5 ${ liked.has(c.id) ? "fill-current" : "" }`} />
                  {c.like_count}
                </button>
                <button className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-white transition-colors">
                  <Share2 className="w-3.5 h-3.5" /> Open
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
'''

# ====================================================================
# PHASE 10 — CIRCUIT EXPORT + QASM IMPORT
# ====================================================================

files[f"{BACK}/app/api/v1/export.py"] = '''
"""Circuit export / import endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.models.user import User
from app.quantum.engine import build_circuit

router = APIRouter(prefix="/export", tags=["export"])


class ExportRequest(BaseModel):
    qubits: int
    classical_bits: int
    operations: list[dict[str, Any]]
    format: str = "qasm"  # qasm | python | json


@router.post("/circuit")
async def export_circuit(body: ExportRequest, user: User = Depends(get_current_user)):
    qc = build_circuit(body.qubits, body.classical_bits, body.operations)

    if body.format == "qasm":
        code = qc.qasm() if hasattr(qc, "qasm") else "# QASM export requires Qiskit 0.x"
        return PlainTextResponse(code, media_type="text/plain")

    elif body.format == "python":
        ops = body.operations
        lines = [
            "from qiskit import QuantumCircuit",
            "from qiskit_aer import AerSimulator",
            "",
            f"qc = QuantumCircuit({body.qubits}, {body.classical_bits})",
        ]
        for op in ops:
            gate = op.get("gate", "").lower()
            targets = op.get("targets", [])
            controls = op.get("controls", [])
            if gate in ("h", "x", "y", "z", "s", "t", "sdg", "tdg") and targets:
                lines.append(f"qc.{gate}({targets[0]})")
            elif gate in ("cnot", "cx") and targets and controls:
                lines.append(f"qc.cx({controls[0]}, {targets[0]})")
            elif gate == "cz" and targets and controls:
                lines.append(f"qc.cz({controls[0]}, {targets[0]})")
            elif gate == "swap" and len(targets) >= 2:
                lines.append(f"qc.swap({targets[0]}, {targets[1]})")
            elif gate == "measure" and targets:
                lines.append(f"qc.measure({targets[0]}, {targets[0]})")
        lines += [
            "",
            "sim    = AerSimulator()",
            "result = sim.run(qc, shots=1024).result()",
            "counts = result.get_counts()",
            "print(counts)",
        ]
        return PlainTextResponse("\n".join(lines), media_type="text/plain")

    elif body.format == "json":
        import json
        return PlainTextResponse(
            json.dumps({"qubits": body.qubits, "classical_bits": body.classical_bits, "operations": body.operations}, indent=2),
            media_type="application/json",
        )

    raise HTTPException(400, "Format must be qasm, python, or json")
'''

files[f"{FRONT}/src/components/quantum-lab/ExportPanel.tsx"] = '''
"use client";
import { useState } from "react";
import { Download, Copy, Check } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";
import { api } from "@/lib/api";

type Format = "qasm" | "python" | "json";

interface ExportPanelProps {
  qubits: number;
  classicalBits: number;
  operations: any[];
}

export function ExportPanel({ qubits, classicalBits, operations }: ExportPanelProps) {
  const [format, setFormat] = useState<Format>("python");
  const [code, setCode]     = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied]   = useState(false);

  async function generate() {
    setLoading(true);
    try {
      const res = await api.post("/export/circuit", { qubits, classical_bits: classicalBits, operations, format });
      setCode(await res.text());
    } finally {
      setLoading(false);
    }
  }

  function copy() {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  function download() {
    const ext = format === "python" ? "py" : format === "json" ? "json" : "qasm";
    const blob = new Blob([code], { type: "text/plain" });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href = url; a.download = `circuit.${ext}`;
    a.click(); URL.revokeObjectURL(url);
  }

  return (
    <div className="glass rounded-xl border border-white/5 p-5">
      <h3 className="text-sm font-semibold text-white mb-4">Export Circuit</h3>

      <div className="flex gap-1 p-1 bg-white/5 rounded-lg mb-4">
        {(["python", "qasm", "json"] as Format[]).map(f => (
          <button key={f} onClick={() => setFormat(f)}
            className={`flex-1 py-1.5 rounded-md text-xs font-medium transition-all ${
              format === f ? "bg-quantum-blue/15 text-quantum-blue" : "text-muted-foreground hover:text-white"
            }`}>
            {f.toUpperCase()}
          </button>
        ))}
      </div>

      <GlowButton onClick={generate} loading={loading} className="w-full justify-center mb-4">
        Generate Code
      </GlowButton>

      {code && (
        <>
          <div className="relative">
            <pre className="p-4 bg-[#0d0d1a] border border-white/10 rounded-xl text-xs text-green-400 overflow-auto max-h-48 font-mono">{code}</pre>
            <button onClick={copy} className="absolute top-2 right-2 p-1.5 bg-white/5 hover:bg-white/10 rounded-md transition">
              {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5 text-muted-foreground" />}
            </button>
          </div>
          <GlowButton variant="secondary" onClick={download} className="w-full justify-center mt-3">
            <Download className="w-4 h-4" /> Download
          </GlowButton>
        </>
      )}
    </div>
  );
}
'''

# ====================================================================
# PHASE 11 — QUANTUM ERROR CORRECTION MODULE
# ====================================================================

files[f"{BACK}/app/quantum/error_correction.py"] = '''
"""Basic quantum error correction circuits."""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


def bit_flip_code(error_qubit: int = 0, apply_error: bool = True) -> dict:
    """3-qubit bit flip code. Encodes 1 logical qubit into 3 physical qubits."""
    qr = QuantumRegister(3, "q")
    anc = QuantumRegister(2, "anc")
    cr = ClassicalRegister(3, "c")
    qc = QuantumCircuit(qr, anc, cr)

    # Encode: |0> -> |000>, |1> -> |111>
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])
    qc.barrier()

    # Simulate a bit-flip error
    if apply_error and 0 <= error_qubit < 3:
        qc.x(qr[error_qubit])
    qc.barrier()

    # Syndrome measurement
    qc.cx(qr[0], anc[0]); qc.cx(qr[1], anc[0])
    qc.cx(qr[1], anc[1]); qc.cx(qr[2], anc[1])
    qc.barrier()

    # Error correction via syndrome
    qc.ccx(anc[0], anc[1], qr[1])  # Correct qubit 1 if both syndromes fire
    qc.barrier()
    qc.measure(qr, cr)

    sim = AerSimulator()
    counts = sim.run(qc, shots=512).result().get_counts(0)
    total = sum(counts.values())

    return {
        "code": "bit_flip",
        "error_qubit": error_qubit,
        "error_applied": apply_error,
        "counts": counts,
        "probabilities": {k: round(v / total, 4) for k, v in counts.items()},
        "success": True,
        "description": "3-qubit bit-flip code: detects and corrects single bit-flip errors.",
    }


def phase_flip_code(apply_error: bool = True) -> dict:
    """3-qubit phase flip (sign flip) code."""
    qr = QuantumRegister(3, "q")
    cr = ClassicalRegister(3, "c")
    qc = QuantumCircuit(qr, cr)

    # Encode in X basis
    qc.h(range(3))
    qc.cx(qr[0], qr[1]); qc.cx(qr[0], qr[2])
    qc.barrier()

    if apply_error:
        qc.z(qr[0])  # Phase flip error on qubit 0
    qc.barrier()

    # Decode
    qc.cx(qr[0], qr[1]); qc.cx(qr[0], qr[2])
    qc.h(range(3))
    qc.barrier()
    qc.measure(qr, cr)

    sim = AerSimulator()
    counts = sim.run(qc, shots=512).result().get_counts(0)
    total = sum(counts.values())
    return {
        "code": "phase_flip",
        "error_applied": apply_error,
        "counts": counts,
        "probabilities": {k: round(v / total, 4) for k, v in counts.items()},
        "success": True,
        "description": "3-qubit phase-flip code: detects and corrects single phase errors.",
    }


def noisy_simulation(qubits: int, operations: list, error_rate: float = 0.01, shots: int = 1024) -> dict:
    """Run a simulation with a depolarizing noise model."""
    from app.quantum.engine import build_circuit

    noise = NoiseModel()
    error = depolarizing_error(error_rate, 1)
    noise.add_all_qubit_quantum_error(error, ["h", "x", "y", "z", "s", "t"])

    qc = build_circuit(qubits, qubits, operations)
    sim = AerSimulator(noise_model=noise)
    counts = sim.run(qc, shots=shots).result().get_counts(0)
    total = sum(counts.values())
    return {
        "success": True,
        "noise_model": "depolarizing",
        "error_rate": error_rate,
        "counts": counts,
        "probabilities": {k: round(v / total, 4) for k, v in counts.items()},
    }
'''

files[f"{FRONT}/src/app/error-correction/page.tsx"] = '''
"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { ShieldCheck, Play } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { PageHeader } from "@/components/ui/PageHeader";
import { GlowButton } from "@/components/shared/GlowButton";
import { api } from "@/lib/api";

const CODES = [
  { id: "bit_flip",   label: "Bit Flip Code",   desc: "3-qubit code for X errors",     qubits: 3 },
  { id: "phase_flip", label: "Phase Flip Code",  desc: "3-qubit code for Z errors",     qubits: 3 },
  { id: "noisy",      label: "Noisy Simulation", desc: "Run circuit with noise model",   qubits: 2 },
];

const TOOLTIP_STYLE = {
  contentStyle: { background: "#0d0d1a", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 12, fontSize: 12 },
  itemStyle: { color: "#00d4ff" },
};

export default function ErrorCorrectionPage() {
  const [selected, setSelected] = useState("bit_flip");
  const [errorQubit, setErrorQubit] = useState(0);
  const [applyError, setApplyError] = useState(true);
  const [result, setResult]   = useState<any>(null);
  const [running, setRunning] = useState(false);

  async function run() {
    setRunning(true);
    try {
      let res;
      if (selected === "bit_flip") {
        res = await api.post("/error-correction/bit-flip",   { error_qubit: errorQubit, apply_error: applyError });
      } else if (selected === "phase_flip") {
        res = await api.post("/error-correction/phase-flip", { apply_error: applyError });
      } else {
        res = await api.post("/error-correction/noisy",      { qubits: 2, operations: [{gate:"H",targets:[0],controls:[],column:0},{gate:"CNOT",targets:[1],controls:[0],column:1}], error_rate: 0.05 });
      }
      setResult(await res.json());
    } finally {
      setRunning(false);
    }
  }

  const chartData = result ? Object.entries(result.probabilities).map(([k, v]) => ({ state: `|${k}\u27e9`, prob: Math.round((v as number) * 100) })) : [];

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <PageHeader icon={<ShieldCheck className="w-6 h-6 text-quantum-blue" />}
        title="Error Correction" subtitle="Understand how quantum computers protect against noise" />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {CODES.map(c => (
          <button key={c.id} onClick={() => setSelected(c.id)}
            className={`p-4 rounded-xl border text-left transition-all ${
              selected === c.id ? "border-quantum-blue bg-quantum-blue/10" : "border-white/5 hover:border-white/20 glass"
            }`}>
            <p className={`font-semibold text-sm mb-1 ${ selected === c.id ? "text-quantum-blue" : "text-white" }`}>{c.label}</p>
            <p className="text-xs text-muted-foreground">{c.desc}</p>
          </button>
        ))}
      </div>

      <div className="glass rounded-xl border border-white/5 p-6 mb-6">
        <h3 className="text-sm font-semibold text-white mb-4">Configuration</h3>
        {selected === "bit_flip" && (
          <div className="flex gap-6 flex-wrap">
            <div>
              <label className="text-xs text-muted-foreground mb-2 block">Error qubit</label>
              <div className="flex gap-2">
                {[0,1,2].map(q => (
                  <button key={q} onClick={() => setErrorQubit(q)}
                    className={`w-10 h-10 rounded-lg font-bold text-sm transition-all ${ errorQubit === q ? "bg-quantum-blue text-quantum-dark" : "bg-white/5 text-muted-foreground hover:bg-white/10" }`}>
                    q{q}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-2 block">Apply error?</label>
              <button onClick={() => setApplyError(p => !p)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${ applyError ? "bg-red-500/20 text-red-400 border border-red-500/30" : "bg-white/5 text-muted-foreground" }`}>
                {applyError ? "Error ON" : "Error OFF"}
              </button>
            </div>
          </div>
        )}
        <GlowButton onClick={run} loading={running} className="mt-5">
          <Play className="w-4 h-4" /> Run Simulation
        </GlowButton>
      </div>

      {result && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          className="glass rounded-xl border border-white/5 p-6">
          <p className="text-xs text-muted-foreground mb-4">{result.description}</p>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={chartData}>
              <XAxis dataKey="state" tick={{ fontSize: 11, fill: "#6b6b80" }} />
              <YAxis unit="%" tick={{ fontSize: 11, fill: "#6b6b80" }} />
              <Tooltip {...TOOLTIP_STYLE} formatter={(v: any) => [`${v}%`, "Probability"]} />
              <Bar dataKey="prob" fill="#00d4ff" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      )}
    </div>
  );
}
'''

# ====================================================================
# PHASE 12 — PWA + MOBILE RESPONSIVE
# ====================================================================

os.makedirs(f"{FRONT}/public", exist_ok=True)
files[f"{FRONT}/public/manifest.json"] = '''{
  "name": "QuantumVerse AI",
  "short_name": "QuantumVerse",
  "description": "AI-Powered Quantum Algorithm Learning Platform",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#080812",
  "theme_color": "#00d4ff",
  "orientation": "portrait-primary",
  "icons": [
    { "src": "/icon-192.png",  "sizes": "192x192",  "type": "image/png", "purpose": "any maskable" },
    { "src": "/icon-512.png",  "sizes": "512x512",  "type": "image/png", "purpose": "any maskable" }
  ],
  "categories": ["education", "science"],
  "screenshots": [
    { "src": "/screenshot-desktop.png", "sizes": "1280x720", "type": "image/png", "form_factor": "wide" },
    { "src": "/screenshot-mobile.png",  "sizes": "390x844",  "type": "image/png", "form_factor": "narrow" }
  ]
}
'''

files[f"{FRONT}/public/sw.js"] = '''
// QuantumVerse Service Worker
const CACHE = "quantumverse-v1";
const STATIC = ["/", "/dashboard", "/offline.html"];

self.addEventListener("install", e =>
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(STATIC)))
);

self.addEventListener("activate", e =>
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ))
);

self.addEventListener("fetch", e => {
  if (e.request.url.includes("/api/")) return; // Never cache API
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (!res || res.status !== 200) return res;
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      }).catch(() => caches.match("/offline.html"));
    })
  );
});
'''

files[f"{FRONT}/src/components/ui/MobileNav.tsx"] = '''
"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, FlaskConical, BookOpen, BrainCircuit, User } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/dashboard",  icon: Home,          label: "Home"  },
  { href: "/quantum-lab", icon: FlaskConical, label: "Lab"   },
  { href: "/learn",      icon: BookOpen,      label: "Learn" },
  { href: "/ai-tutor",   icon: BrainCircuit,  label: "AI"   },
  { href: "/profile",    icon: User,          label: "Me"   },
];

export function MobileNav() {
  const path = usePathname();
  return (
    <nav className="md:hidden fixed bottom-0 inset-x-0 z-50 glass border-t border-white/5 flex">
      {NAV.map(({ href, icon: Icon, label }) => {
        const active = path === href || (href !== "/dashboard" && path.startsWith(href));
        return (
          <Link key={href} href={href}
            className={cn("flex-1 flex flex-col items-center gap-0.5 py-3 transition-colors",
              active ? "text-quantum-blue" : "text-muted-foreground hover:text-white")}>
            <Icon className="w-5 h-5" />
            <span className="text-[10px] font-medium">{label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
'''

# ====================================================================
# PHASE 13 — AI CIRCUIT GENERATOR
# ====================================================================

files[f"{BACK}/app/api/v1/ai_circuit.py"] = '''
"""AI-powered circuit generation from natural language."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.models.user import User
from app.ai.provider import get_ai_response

router = APIRouter(prefix="/ai-circuit", tags=["ai_circuit"])

CIRCUIT_TEMPLATES = {
    "bell": {
        "name": "Bell State",
        "qubits": 2, "classical_bits": 2,
        "operations": [
            {"gate": "H",    "targets": [0], "controls": [], "column": 0},
            {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1},
        ]
    },
    "ghz": {
        "name": "GHZ State",
        "qubits": 3, "classical_bits": 3,
        "operations": [
            {"gate": "H",    "targets": [0], "controls": [],  "column": 0},
            {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1},
            {"gate": "CNOT", "targets": [2], "controls": [0], "column": 2},
        ]
    },
    "superposition": {
        "name": "Equal Superposition",
        "qubits": 2, "classical_bits": 2,
        "operations": [
            {"gate": "H", "targets": [0], "controls": [], "column": 0},
            {"gate": "H", "targets": [1], "controls": [], "column": 0},
        ]
    },
    "qft_2": {
        "name": "2-Qubit QFT",
        "qubits": 2, "classical_bits": 2,
        "operations": [
            {"gate": "H",  "targets": [0], "controls": [],  "column": 0},
            {"gate": "RZ", "targets": [1], "controls": [],  "column": 0, "params": {"angle": 1.5707963}},
            {"gate": "H",  "targets": [1], "controls": [],  "column": 1},
            {"gate": "SWAP","targets": [0,1], "controls": [], "column": 2},
        ]
    },
}

KEYWORDS = {
    "bell":          ["bell", "entangle", "maximize", "max entangl"],
    "ghz":           ["ghz", "3 qubit entangle", "three qubit"],
    "superposition": ["superpos", "both states", "hadamard"],
    "qft_2":         ["fourier", "qft"],
}


class GenerateRequest(BaseModel):
    description: str
    difficulty: str = "beginner"


@router.post("/generate")
async def generate_circuit(body: GenerateRequest, user: User = Depends(get_current_user)):
    desc_lower = body.description.lower()

    # First try keyword matching
    for key, words in KEYWORDS.items():
        if any(w in desc_lower for w in words):
            tpl = CIRCUIT_TEMPLATES[key].copy()
            tpl["source"] = "template"
            tpl["explanation"] = await get_ai_response(
                f"Explain briefly what a {tpl[\'name\']} circuit does for a {body.difficulty} student.",
                [], body.difficulty
            )
            return tpl

    # Fall back to default with AI explanation
    tpl = CIRCUIT_TEMPLATES["bell"].copy()
    tpl["source"] = "fallback"
    tpl["explanation"] = (
        "I\'ve loaded a Bell State circuit as a starting point. "
        "Describe something more specific like \'GHZ state\', \'superposition\', or \'QFT\' for a custom circuit."
    )
    return tpl
'''

files[f"{FRONT}/src/components/quantum-lab/AICircuitGenerator.tsx"] = '''
"use client";
import { useState } from "react";
import { Wand2, Loader2 } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";
import { api } from "@/lib/api";

interface AICircuitGeneratorProps {
  onGenerated: (circuit: any) => void;
}

const EXAMPLES = [
  "Create a Bell state circuit",
  "Build a 3-qubit GHZ state",
  "Make a superposition of all states",
  "Show me a 2-qubit QFT",
];

export function AICircuitGenerator({ onGenerated }: AICircuitGeneratorProps) {
  const [prompt,  setPrompt]  = useState("");
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState("");

  async function generate() {
    if (!prompt.trim()) return;
    setLoading(true); setError("");
    try {
      const res = await api.post("/ai-circuit/generate", { description: prompt });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      onGenerated(data);
      setPrompt("");
    } catch (e: any) {
      setError(e.message ?? "Generation failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="glass rounded-xl border border-white/5 p-5">
      <div className="flex items-center gap-2 mb-3">
        <Wand2 className="w-4 h-4 text-quantum-blue" />
        <h3 className="text-sm font-semibold text-white">AI Circuit Generator</h3>
      </div>

      <div className="flex gap-2 mb-3">
        <input
          value={prompt} onChange={e => setPrompt(e.target.value)}
          onKeyDown={e => e.key === "Enter" && generate()}
          placeholder="Describe a circuit in plain English..."
          className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-quantum-blue/50"
        />
        <GlowButton onClick={generate} loading={loading} disabled={!prompt.trim()}>
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Wand2 className="w-4 h-4" />}
        </GlowButton>
      </div>

      {error && <p className="text-red-400 text-xs mb-3">{error}</p>}

      <div className="flex flex-wrap gap-2">
        {EXAMPLES.map(ex => (
          <button key={ex} onClick={() => setPrompt(ex)}
            className="text-xs px-2.5 py-1 rounded-full border border-white/10 text-muted-foreground hover:border-quantum-blue/30 hover:text-quantum-blue transition-colors">
            {ex}
          </button>
        ))}
      </div>
    </div>
  );
}
'''

# ====================================================================
# PHASE 14 — REDIS CACHING + RATE LIMITING + PERFORMANCE
# ====================================================================

files[f"{BACK}/app/core/cache.py"] = '''
"""Redis cache abstraction (falls back to in-memory if Redis unavailable)."""
import json
import asyncio
import time
from typing import Any
from app.core.config import settings
import logging

log = logging.getLogger(__name__)

_memory: dict[str, tuple[Any, float]] = {}


try:
    import redis.asyncio as aioredis
    _redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=2)
    _use_redis = True
except Exception:
    _use_redis = False
    log.info("Redis unavailable, using in-memory cache.")


async def get(key: str) -> Any | None:
    if _use_redis:
        try:
            val = await _redis_client.get(key)
            return json.loads(val) if val else None
        except Exception:
            pass
    val, exp = _memory.get(key, (None, 0))
    return val if exp > time.time() else None


async def set(key: str, value: Any, ttl: int = 300) -> None:
    if _use_redis:
        try:
            await _redis_client.setex(key, ttl, json.dumps(value))
            return
        except Exception:
            pass
    _memory[key] = (value, time.time() + ttl)


async def delete(key: str) -> None:
    if _use_redis:
        try:
            await _redis_client.delete(key)
        except Exception:
            pass
    _memory.pop(key, None)


async def cache_simulation(circuit_hash: str, result: dict, ttl: int = 600) -> None:
    await set(f"sim:{circuit_hash}", result, ttl)

async def get_cached_simulation(circuit_hash: str) -> dict | None:
    return await get(f"sim:{circuit_hash}")
'''

files[f"{BACK}/app/core/rate_limit.py"] = '''
"""Simple in-memory + Redis rate limiter."""
import time
from collections import defaultdict
from fastapi import Request, HTTPException
from app.core.cache import get, set

_local: dict[str, list[float]] = defaultdict(list)


async def rate_limit(request: Request, limit: int = 60, window: int = 60):
    """Allow `limit` requests per `window` seconds per IP. Use as a FastAPI dependency."""
    ip = request.client.host if request.client else "unknown"
    key = f"rl:{ip}"

    now = time.time()
    hits = _local[key]
    hits[:] = [t for t in hits if t > now - window]

    if len(hits) >= limit:
        raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")

    hits.append(now)


async def simulation_rate_limit(request: Request):
    """Stricter limit for compute-heavy simulation endpoints: 20/min."""
    await rate_limit(request, limit=20, window=60)
'''

files[f"{FRONT}/src/components/shared/SkeletonCard.tsx"] = '''
export function SkeletonCard({ lines = 3, className = "" }: { lines?: number; className?: string }) {
  return (
    <div className={`glass rounded-xl border border-white/5 p-5 animate-pulse ${className}`}>
      <div className="h-4 bg-white/5 rounded-full w-3/4 mb-3" />
      {[...Array(lines - 1)].map((_, i) => (
        <div key={i} className={`h-3 bg-white/5 rounded-full mb-2 ${ i === lines - 2 ? "w-1/2" : "w-full" }`} />
      ))}
    </div>
  );
}

export function SkeletonGrid({ count = 6, className = "" }: { count?: number; className?: string }) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 ${className}`}>
      {[...Array(count)].map((_, i) => <SkeletonCard key={i} />)}
    </div>
  );
}
'''

# ====================================================================
# PHASE 15 — MONITORING + ERROR PAGES + FINAL POLISH
# ====================================================================

files[f"{BACK}/app/api/v1/health.py"] = '''
"""Health check and metrics endpoints."""
import time
import platform
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="/system", tags=["system"])
_start_time = time.time()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
        "uptime_seconds": round(time.time() - _start_time),
        "python": platform.python_version(),
    }


@router.get("/metrics")
async def metrics():
    """Basic Prometheus-style text metrics."""
    uptime = round(time.time() - _start_time)
    lines = [
        "# HELP quantumverse_uptime_seconds Total uptime in seconds",
        "# TYPE quantumverse_uptime_seconds gauge",
        f"quantumverse_uptime_seconds {uptime}",
        "",
        "# HELP quantumverse_info Version info",
        "# TYPE quantumverse_info gauge",
        f"quantumverse_info{{version=\\"{settings.APP_VERSION}\\"}} 1",
    ]
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse("\n".join(lines), media_type="text/plain; version=0.0.4")
'''

files[f"{FRONT}/src/app/not-found.tsx"] = '''
import Link from "next/link";
import { Home, AtomIcon } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center px-4 bg-quantum-dark">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[400px] h-[400px] rounded-full bg-quantum-blue/5 blur-3xl" />
      </div>
      <p className="text-8xl font-black text-quantum-blue/20 mb-4">404</p>
      <h1 className="text-2xl font-bold text-white mb-2">This state has collapsed</h1>
      <p className="text-muted-foreground text-sm mb-8 max-w-sm">
        Like a measured qubit, this page only exists in superposition. Try navigating back.
      </p>
      <Link href="/dashboard"
        className="flex items-center gap-2 px-6 py-3 rounded-xl bg-quantum-blue text-quantum-dark font-semibold text-sm hover:opacity-90 transition-opacity">
        <Home className="w-4 h-4" /> Back to Dashboard
      </Link>
    </div>
  );
}
'''

files[f"{FRONT}/src/app/error.tsx"] = '''
"use client";
import { useEffect } from "react";
import { RefreshCw } from "lucide-react";

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => { console.error(error); }, [error]);
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center px-4">
      <p className="text-6xl mb-4">⚠️</p>
      <h2 className="text-xl font-bold text-white mb-2">Something went wrong</h2>
      <p className="text-muted-foreground text-sm mb-6 max-w-sm">{error.message || "An unexpected error occurred."}</p>
      <button onClick={reset}
        className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-quantum-blue text-quantum-dark font-semibold text-sm">
        <RefreshCw className="w-4 h-4" /> Try Again
      </button>
    </div>
  );
}
'''

files[f"{FRONT}/src/components/shared/ErrorBoundary.tsx"] = '''
"use client";
import React, { Component, ReactNode } from "react";

interface Props { children: ReactNode; fallback?: ReactNode; }
interface State { hasError: boolean; error?: Error; }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("ErrorBoundary caught:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div className="p-6 text-center text-muted-foreground">
          <p className="text-2xl mb-2">⚠️</p>
          <p className="text-sm">{this.state.error?.message ?? "Something went wrong."}</p>
          <button onClick={() => this.setState({ hasError: false })}
            className="mt-3 text-xs text-quantum-blue hover:underline">Try again</button>
        </div>
      );
    }
    return this.props.children;
  }
}
'''

files[f"{FRONT}/src/app/offline.html"] = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Offline — QuantumVerse AI</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #080812; color: #fff; font-family: sans-serif;
           display: flex; align-items: center; justify-content: center; min-height: 100vh; text-align: center; padding: 24px; }
    h1 { color: #00d4ff; font-size: 2rem; margin-bottom: 12px; }
    p  { color: #6b6b80; margin-bottom: 24px; }
    button { background: #00d4ff; color: #080812; border: none; padding: 12px 28px;
             border-radius: 10px; font-weight: 700; cursor: pointer; font-size: 14px; }
  </style>
</head>
<body>
  <div>
    <div style="font-size:4rem;margin-bottom:16px">🔬</div>
    <h1>You\'re Offline</h1>
    <p>Your connection collapsed into an eigenstate of ‘disconnected\'.<br/>Check your internet and try again.</p>
    <button onclick="window.location.reload()">Reconnect</button>
  </div>
</body>
</html>
'''

# ====================================================================
# ALEMBIC MIGRATION SETUP
# ====================================================================

files[f"{BACK}/alembic.ini"] = '''
[alembic]
script_location = alembic
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s
timezone = UTC
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = postgresql+asyncpg://postgres:password@localhost:5432/quantumverse

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %%H:%%M:%%S
'''

os.makedirs(f"{BACK}/alembic/versions", exist_ok=True)
files[f"{BACK}/alembic/env.py"] = '''
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models.user        import Base as UserBase
from app.models.circuit     import Base as CircuitBase
from app.models.learning    import Base as LearningBase
from app.models.quiz        import Base as QuizBase
from app.models.achievement import Base as AchievementBase
from app.models.ai          import Base as AIBase

target_metadata = [UserBase.metadata, CircuitBase.metadata, LearningBase.metadata,
                   QuizBase.metadata, AchievementBase.metadata, AIBase.metadata]


def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    cfg = config.get_section(config.config_ini_section)
    connectable = async_engine_from_config(cfg, prefix="sqlalchemy.", poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(lambda conn: context.configure(connection=conn, target_metadata=target_metadata))
        async with connection.begin():
            await connection.run_sync(lambda _: context.run_migrations())
    await connectable.dispose()


def run_migrations_online():
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''

# ====================================================================
# FINAL CONFIG ADDITIONS
# ====================================================================

files[f"{BACK}/app/core/config.py"] = '''
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str    = "QuantumVerse AI"
    APP_VERSION: str = "2.0.0"
    APP_URL: str     = "https://quantumverse.ai"
    DEBUG: bool      = False

    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/quantumverse"

    SECRET_KEY: str  = "change-me-in-production-use-256-bit-random-key"
    ALGORITHM: str   = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    OPENROUTER_API_KEY: str = "your-openrouter-key-here"
    AI_MODEL: str           = "meta-llama/llama-3.1-8b-instruct:free"

    REDIS_URL: str = "redis://localhost:6379/0"

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    SMTP_FROM: str = "noreply@quantumverse.ai"

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://quantumverse.vercel.app",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
'''

# Updated .env.example with all new vars
files[f"{BACK}/.env.example"] = '''
# ────────────── Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/quantumverse
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=quantumverse

# ────────────── Auth (generate: openssl rand -hex 32)
SECRET_KEY=change-me-to-a-random-256-bit-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# ────────────── AI (free at https://openrouter.ai)
OPENROUTER_API_KEY=your-openrouter-key-here
AI_MODEL=meta-llama/llama-3.1-8b-instruct:free

# ────────────── Redis (optional — falls back to in-memory)
REDIS_URL=redis://localhost:6379/0

# ────────────── Email (optional — SMTP for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=noreply@quantumverse.ai

# ────────────── App
APP_URL=https://quantumverse.ai
DEBUG=false
CORS_ORIGINS=["http://localhost:3000","https://quantumverse.vercel.app"]
'''

# ───────────────────────────────────────────────────────────────────────
# Write all files
# ───────────────────────────────────────────────────────────────────────
written = 0
phase_counts = {8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}

PHASE_MAP = {
    "email": 8, "onboarding": 8,
    "community": 9,
    "export": 10, "ExportPanel": 10,
    "error_correction": 11, "error-correction": 11,
    "manifest": 12, "sw.js": 12, "MobileNav": 12, "offline": 12,
    "ai_circuit": 13, "AICircuitGenerator": 13,
    "cache": 14, "rate_limit": 14, "Skeleton": 14,
    "health": 15, "not-found": 15, "error.tsx": 15, "ErrorBoundary": 15,
    "alembic": 15, "config": 15, ".env.example": 8,
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', errors='replace') as f:
        f.write(content.lstrip('\n'))
    rel = path.replace('/data/quantumverse/', '')
    cat = 'FE' if 'frontend' in path else 'BE' if 'backend' in path else 'ROOT'

    # Figure out phase
    phase = 15
    for key, p in PHASE_MAP.items():
        if key in rel:
            phase = p
            break
    phase_counts[phase] = phase_counts.get(phase, 0) + 1

    print(f"  [P{phase}] {cat}: {rel}")
    written += 1

print(f"\n{'='*60}")
print(f"Total files written: {written}")
for p, c in phase_counts.items():
    if c:
        print(f"  Phase {p}: {c} file(s)")
