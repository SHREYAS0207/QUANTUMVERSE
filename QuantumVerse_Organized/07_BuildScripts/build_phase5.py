import os

BASE = "/data/quantumverse"
FRONT = f"{BASE}/frontend"
BACK  = f"{BASE}/backend"

files = {}

# ======================================================================
# BACKEND: Rich Lesson Seed Data
# ======================================================================

files[f"{BACK}/app/data/lessons_seed.py"] = '''
"""Lesson seed data — run once via seed.py"""

MODULES = [
    {
        "title": "Quantum Fundamentals",
        "description": "Master the building blocks of quantum computing from scratch.",
        "level": "beginner",
        "icon": "atom",
        "order_index": 1,
        "lessons": [
            {
                "title": "What is a Qubit?",
                "order_index": 1,
                "xp_reward": 50,
                "estimated_minutes": 8,
                "content": """
# What is a Qubit?

A **qubit** (quantum bit) is the fundamental unit of quantum information, the quantum analogue of a classical bit.

## Classical Bits vs Qubits

A classical bit is always in one of two definite states:
- `0` — off
- `1` — on

A qubit, however, can exist in a **superposition** of both states simultaneously. We write this using **Dirac notation** (ket notation):

$$|\\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle$$

Where:
- $|0\\rangle$ and $|1\\rangle$ are the **basis states**
- $\\alpha$ and $\\beta$ are complex **probability amplitudes**
- The probabilities must sum to 1: $|\\alpha|^2 + |\\beta|^2 = 1$

## The Bloch Sphere

Every pure qubit state can be visualised as a point on the **Bloch sphere**:

- **North pole** → $|0\\rangle$ (probability 1 of measuring 0)
- **South pole** → $|1\\rangle$ (probability 1 of measuring 1)
- **Equator** → equal superposition states like $|+\\rangle = \\frac{1}{\\sqrt{2}}(|0\\rangle + |1\\rangle)$

## Creating a Qubit in Qiskit

```python
from qiskit import QuantumCircuit

# Create a 1-qubit circuit
qc = QuantumCircuit(1, 1)

# Qubit starts in |0> by default
print(qc.draw())

# Apply Hadamard to create superposition
qc.h(0)
print("After H gate:", qc.draw())
```

## Key Takeaways

- Qubits are described by quantum state vectors
- Measurement **collapses** the superposition to 0 or 1 with probabilities $|\\alpha|^2$ and $|\\beta|^2$
- Before measurement, the qubit is genuinely in both states at once
- This is not like a coin — quantum superposition has measurable interference effects
""",
            },
            {
                "title": "Superposition & Measurement",
                "order_index": 2,
                "xp_reward": 60,
                "estimated_minutes": 10,
                "content": """
# Superposition & Measurement

## What is Quantum Superposition?

Superposition is one of the most counter-intuitive principles in quantum mechanics. Unlike classical probability ("the coin *is* heads, we just don\'t know"), a qubit in superposition is *genuinely* in multiple states simultaneously.

## The Hadamard Gate

The most common way to create superposition is the **Hadamard gate (H)**:

$$H = \\frac{1}{\\sqrt{2}}\\begin{pmatrix}1 & 1 \\\\ 1 & -1\\end{pmatrix}$$

Applied to $|0\\rangle$:
$$H|0\\rangle = \\frac{1}{\\sqrt{2}}(|0\\rangle + |1\\rangle) = |+\\rangle$$

Applied to $|1\\rangle$:
$$H|1\\rangle = \\frac{1}{\\sqrt{2}}(|0\\rangle - |1\\rangle) = |-\\rangle$$

## Measurement & Wave Function Collapse

When we **measure** a qubit:
1. The superposition collapses to $|0\\rangle$ or $|1\\rangle$
2. Probability of $|0\\rangle$ = $|\\alpha|^2$, probability of $|1\\rangle$ = $|\\beta|^2$
3. The original state is **destroyed** — you cannot clone an unknown quantum state

## Try It in Qiskit

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(1, 1)
qc.h(0)          # Create superposition
qc.measure(0, 0) # Measure

sim = AerSimulator()
result = sim.run(qc, shots=1000).result()
counts = result.get_counts()
print(counts)  # ~{'0': 500, '1': 500}
```

## The No-Cloning Theorem

You **cannot** copy an arbitrary unknown qubit state. This is the **quantum no-cloning theorem** and it has profound implications:
- Quantum states cannot be perfectly copied
- This is what makes quantum cryptography provably secure
- But it enables quantum teleportation!
""",
            },
            {
                "title": "Quantum Gates",
                "order_index": 3,
                "xp_reward": 80,
                "estimated_minutes": 12,
                "content": """
# Quantum Gates

Quantum gates are the quantum equivalent of classical logic gates. They are **unitary matrices** that transform qubit states reversibly.

## Single-Qubit Gates

### Pauli Gates

**X gate** (NOT gate): Flips $|0\\rangle \\leftrightarrow |1\\rangle$
$$X = \\begin{pmatrix}0 & 1 \\\\ 1 & 0\\end{pmatrix}$$

**Y gate**: Combines X and Z with a phase
$$Y = \\begin{pmatrix}0 & -i \\\\ i & 0\\end{pmatrix}$$

**Z gate** (Phase flip): $|0\\rangle \\to |0\\rangle$, $|1\\rangle \\to -|1\\rangle$
$$Z = \\begin{pmatrix}1 & 0 \\\\ 0 & -1\\end{pmatrix}$$

### Phase Gates

**S gate** ($\\sqrt{Z}$): 90° phase rotation on $|1\\rangle$
**T gate** ($\\sqrt{S}$): 45° phase rotation on $|1\\rangle$ — essential for universality!

### Rotation Gates

Parametrised rotations around each Bloch sphere axis:
$$R_X(\\theta) = e^{-i\\theta X/2}, \\quad R_Y(\\theta) = e^{-i\\theta Y/2}, \\quad R_Z(\\theta) = e^{-i\\theta Z/2}$$

## Two-Qubit Gates

### CNOT (Controlled-NOT)
Flips the **target** qubit when the **control** qubit is $|1\\rangle$:

$$CNOT = \\begin{pmatrix}1&0&0&0 \\\\ 0&1&0&0 \\\\ 0&0&0&1 \\\\ 0&0&1&0\\end{pmatrix}$$

Combining H + CNOT creates the **Bell state** (maximum entanglement):

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(2, 2)
qc.h(0)       # Superpose qubit 0
qc.cx(0, 1)   # Entangle qubit 1 with qubit 0
qc.measure_all()
# Result: only |00> and |11> — never |01> or |10>!
```

## Universality

Any quantum computation can be decomposed into:
- Single-qubit rotations ($R_X$, $R_Y$, $R_Z$)
- The CNOT gate

This is the quantum equivalent of NAND completeness in classical computing.
""",
            },
        ],
    },
    {
        "title": "Quantum Entanglement",
        "description": "Explore the spooky action at a distance and its computational power.",
        "level": "beginner",
        "icon": "link",
        "order_index": 2,
        "lessons": [
            {
                "title": "Bell States",
                "order_index": 1,
                "xp_reward": 100,
                "estimated_minutes": 12,
                "content": """
# Bell States

Bell states are the four **maximally entangled** two-qubit states. They form the cornerstone of quantum communication and cryptography.

## The Four Bell States

$$|\\Phi^+\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle + |11\\rangle)$$
$$|\\Phi^-\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle - |11\\rangle)$$
$$|\\Psi^+\\rangle = \\frac{1}{\\sqrt{2}}(|01\\rangle + |10\\rangle)$$
$$|\\Psi^-\\rangle = \\frac{1}{\\sqrt{2}}(|01\\rangle - |10\\rangle)$$

## Creating $|\\Phi^+\\rangle$

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)
qc.h(0)       # Hadamard on qubit 0
qc.cx(0, 1)   # CNOT: control=0, target=1
qc.measure([0,1], [0,1])

sim = AerSimulator()
counts = sim.run(qc, shots=1024).result().get_counts()
print(counts)  # {'00': ~512, '11': ~512}  — never 01 or 10!
```

## What Makes It Special?

In the Bell state $|\\Phi^+\\rangle$:
- If you measure qubit 0 and get **0**, qubit 1 is *instantly* **0**
- If you measure qubit 0 and get **1**, qubit 1 is *instantly* **1**
- This correlation is **perfect** regardless of the distance between qubits
- Einstein called this "spooky action at a distance"

## Bell\'s Theorem

John Bell proved in 1964 that these correlations **cannot be explained** by any classical hidden variable theory. Experimental tests (Aspect, 1982; Hensen, 2015) confirm: **quantum entanglement is real and non-local**.
""",
            },
        ],
    },
    {
        "title": "Quantum Algorithms",
        "description": "Learn the algorithms that give quantum computers their power.",
        "level": "intermediate",
        "icon": "cpu",
        "order_index": 3,
        "lessons": [
            {
                "title": "Grover\'s Algorithm",
                "order_index": 1,
                "xp_reward": 150,
                "estimated_minutes": 15,
                "content": """
# Grover\'s Search Algorithm

Grover\'s algorithm provides a **quadratic speedup** for searching an unstructured database.

## The Problem

Given an unsorted list of $N$ items with one marked item, find it.

- **Classical**: $O(N)$ queries (check each item)
- **Grover**: $O(\\sqrt{N})$ queries

For $N = 10^6$: classical needs up to 1,000,000 checks; Grover needs ~1,000.

## How It Works

Grover\'s algorithm amplifies the amplitude of the target state through two operations:

### 1. The Oracle
Marks the target state $|x^*\\rangle$ with a phase flip:
$$O|x\\rangle = \\begin{cases} -|x\\rangle & \\text{if } x = x^* \\\\ |x\\rangle & \\text{otherwise} \\end{cases}$$

### 2. The Diffusion Operator
Reflects all amplitudes about the average:
$$D = 2|+\\rangle\\langle+| - I$$

Each iteration of Oracle + Diffusion **increases** the target amplitude by $\\sim \\frac{2}{\\sqrt{N}}$.

After $k = \\frac{\\pi}{4}\\sqrt{N}$ iterations, the probability peaks near 1.

## Qiskit Implementation

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import math

def grover_circuit(n: int, target: int) -> QuantumCircuit:
    qc = QuantumCircuit(n, n)
    qc.h(range(n))  # Equal superposition
    
    iterations = round(math.pi / 4 * math.sqrt(2**n))
    for _ in range(iterations):
        # Oracle: phase-flip target state
        target_bits = format(target, f"0{n}b")
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)
        
        # Diffusion operator
        qc.h(range(n))
        qc.x(range(n))
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
        qc.x(range(n))
        qc.h(range(n))
    
    qc.measure(range(n), range(n))
    return qc

qc = grover_circuit(3, 5)  # Find item 5 in 8-item list
sim = AerSimulator()
counts = sim.run(qc, shots=1024).result().get_counts()
print(counts)  # {"101": ~950, ...rest tiny}
```
""",
            },
        ],
    },
]


def get_seed_data():
    return MODULES
'''

# ======================================================================
# FRONTEND: Lesson Viewer Page
# ======================================================================

files[f"{FRONT}/src/app/learn/[moduleId]/page.tsx"] = '''
"use client";
import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { ArrowLeft, ArrowRight, CheckCircle, Clock, Zap } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";
import { XPToast } from "@/components/shared/XPToast";
import { LessonContent } from "@/components/learn/LessonContent";
import { LessonSidebar } from "@/components/learn/LessonSidebar";
import { useLearning } from "@/hooks/useLearning";

export default function ModulePage() {
  const { moduleId } = useParams<{ moduleId: string }>();
  const router = useRouter();
  const { module, lessons, completedIds, completeLesson, loading } = useLearning(moduleId);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [xp, setXp] = useState(0);
  const [showXP, setShowXP] = useState(false);
  const [completing, setCompleting] = useState(false);

  if (loading) return <div className="min-h-screen flex items-center justify-center text-muted-foreground">Loading module...</div>;
  if (!module) return <div className="min-h-screen flex items-center justify-center text-red-400">Module not found.</div>;

  const currentLesson = lessons[currentIndex];
  const isCompleted = currentLesson ? completedIds.includes(currentLesson.id) : false;

  async function handleComplete() {
    if (!currentLesson || isCompleted || completing) return;
    setCompleting(true);
    const earned = await completeLesson(currentLesson.id);
    setXp(earned);
    setShowXP(true);
    setCompleting(false);
    setTimeout(() => setShowXP(false), 3000);
  }

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <LessonSidebar
        module={module}
        lessons={lessons}
        currentIndex={currentIndex}
        completedIds={completedIds}
        onSelect={setCurrentIndex}
      />

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <div className="flex items-center justify-between p-4 border-b border-white/5 glass">
          <button onClick={() => router.push("/learn")} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" />
            Back to modules
          </button>
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            {currentLesson && (
              <>
                <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" />{currentLesson.estimated_minutes} min</span>
                <span className="flex items-center gap-1"><Zap className="w-3.5 h-3.5 text-quantum-blue" />+{currentLesson.xp_reward} XP</span>
              </>
            )}
            <span className="text-muted-foreground/50">{currentIndex + 1} / {lessons.length}</span>
          </div>
        </div>

        {/* Lesson */}
        <div className="flex-1 overflow-y-auto">
          {currentLesson && (
            <motion.div key={currentLesson.id} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.25 }}
              className="max-w-3xl mx-auto px-6 py-10">
              <LessonContent content={currentLesson.content} />

              {/* Actions */}
              <div className="mt-10 flex items-center justify-between">
                <GlowButton variant="ghost" disabled={currentIndex === 0}
                  onClick={() => setCurrentIndex(i => i - 1)}>
                  <ArrowLeft className="w-4 h-4" /> Previous
                </GlowButton>

                <div className="flex gap-3">
                  {!isCompleted ? (
                    <GlowButton onClick={handleComplete} loading={completing}>
                      <CheckCircle className="w-4 h-4" /> Mark Complete
                    </GlowButton>
                  ) : (
                    <div className="flex items-center gap-2 text-green-400 text-sm font-medium">
                      <CheckCircle className="w-4 h-4" /> Completed!
                    </div>
                  )}

                  {currentIndex < lessons.length - 1 && (
                    <GlowButton variant="secondary" onClick={() => setCurrentIndex(i => i + 1)}>
                      Next <ArrowRight className="w-4 h-4" />
                    </GlowButton>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>

      <XPToast xp={xp} visible={showXP} />
    </div>
  );
}
'''

files[f"{FRONT}/src/components/learn/LessonContent.tsx"] = '''
"use client";
import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { Copy, Check } from "lucide-react";
import { useState } from "react";

interface LessonContentProps {
  content: string;
}

function CopyButton({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);
  function copy() {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }
  return (
    <button onClick={copy}
      className="absolute top-3 right-3 p-1.5 rounded-md bg-white/5 hover:bg-white/10 text-muted-foreground hover:text-white transition-colors">
      {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
    </button>
  );
}

export function LessonContent({ content }: LessonContentProps) {
  return (
    <article className="prose prose-invert prose-quantum max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          code({ node, inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || "");
            const code = String(children).replace(/\n$/, "");
            if (!inline && match) {
              return (
                <div className="relative group my-5">
                  <div className="absolute top-0 left-0 px-3 py-1 text-xs text-muted-foreground font-mono bg-white/5 rounded-tl-lg rounded-br-lg">
                    {match[1]}
                  </div>
                  <SyntaxHighlighter
                    style={vscDarkPlus as any}
                    language={match[1]}
                    PreTag="div"
                    className="!rounded-xl !bg-[#0d0d1a] !border !border-white/10 !pt-8"
                    {...props}
                  >
                    {code}
                  </SyntaxHighlighter>
                  <CopyButton code={code} />
                </div>
              );
            }
            return (
              <code className="px-1.5 py-0.5 rounded bg-white/10 text-quantum-blue font-mono text-sm" {...props}>
                {children}
              </code>
            );
          },
          h1: ({ children }) => <h1 className="text-3xl font-bold text-white mb-6 mt-0">{children}</h1>,
          h2: ({ children }) => <h2 className="text-xl font-semibold text-white/90 mb-4 mt-8 pb-2 border-b border-white/10">{children}</h2>,
          h3: ({ children }) => <h3 className="text-lg font-semibold text-white/80 mb-3 mt-6">{children}</h3>,
          p:  ({ children }) => <p className="text-muted-foreground leading-relaxed mb-4">{children}</p>,
          ul: ({ children }) => <ul className="space-y-1 mb-4 pl-4">{children}</ul>,
          ol: ({ children }) => <ol className="space-y-1 mb-4 pl-4 list-decimal">{children}</ol>,
          li: ({ children }) => <li className="text-muted-foreground flex gap-2"><span className="text-quantum-blue mt-1">›</span><span>{children}</span></li>,
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-quantum-blue pl-4 py-1 my-4 bg-quantum-blue/5 rounded-r-lg text-muted-foreground italic">
              {children}
            </blockquote>
          ),
          strong: ({ children }) => <strong className="text-white font-semibold">{children}</strong>,
          table: ({ children }) => (
            <div className="overflow-x-auto my-6">
              <table className="w-full border-collapse border border-white/10 rounded-lg overflow-hidden">{children}</table>
            </div>
          ),
          th: ({ children }) => <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase bg-white/5 border-b border-white/10">{children}</th>,
          td: ({ children }) => <td className="px-4 py-3 text-sm text-muted-foreground border-b border-white/5">{children}</td>,
        }}
      >
        {content}
      </ReactMarkdown>
    </article>
  );
}
'''

files[f"{FRONT}/src/components/learn/LessonSidebar.tsx"] = '''
"use client";
import { CheckCircle, Circle, Lock } from "lucide-react";
import { cn } from "@/lib/utils";

interface Lesson { id: string; title: string; estimated_minutes: number; xp_reward: number; }
interface Module  { title: string; level: string; }

interface LessonSidebarProps {
  module: Module;
  lessons: Lesson[];
  currentIndex: number;
  completedIds: string[];
  onSelect: (i: number) => void;
}

const LEVEL_COLORS: Record<string, string> = {
  beginner:     "text-green-400 bg-green-400/10",
  intermediate: "text-yellow-400 bg-yellow-400/10",
  advanced:     "text-red-400 bg-red-400/10",
};

export function LessonSidebar({ module, lessons, currentIndex, completedIds, onSelect }: LessonSidebarProps) {
  return (
    <aside className="w-72 flex-shrink-0 glass border-r border-white/5 overflow-y-auto flex flex-col">
      {/* Module header */}
      <div className="p-5 border-b border-white/5">
        <h2 className="font-bold text-white text-sm leading-tight mb-2">{module.title}</h2>
        <span className={cn("text-xs font-medium px-2 py-0.5 rounded-full", LEVEL_COLORS[module.level] ?? "text-blue-400 bg-blue-400/10")}>
          {module.level}
        </span>
      </div>

      {/* Progress bar */}
      <div className="px-5 pt-4 pb-2">
        <div className="flex justify-between text-xs text-muted-foreground mb-1.5">
          <span>Progress</span>
          <span>{completedIds.length} / {lessons.length}</span>
        </div>
        <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
          <div
            className="h-full bg-quantum-blue rounded-full transition-all duration-500"
            style={{ width: `${lessons.length ? completedIds.length / lessons.length * 100 : 0}%` }}
          />
        </div>
      </div>

      {/* Lesson list */}
      <nav className="flex-1 p-3 space-y-1">
        {lessons.map((lesson, i) => {
          const done    = completedIds.includes(lesson.id);
          const active  = i === currentIndex;
          const locked  = i > 0 && !completedIds.includes(lessons[i - 1].id) && !done;

          return (
            <button
              key={lesson.id}
              onClick={() => !locked && onSelect(i)}
              disabled={locked}
              className={cn(
                "w-full text-left px-3 py-2.5 rounded-lg transition-all",
                active  ? "bg-quantum-blue/10 border border-quantum-blue/30 text-white" :
                done    ? "text-muted-foreground hover:bg-white/5 hover:text-white" :
                locked  ? "text-muted-foreground/40 cursor-not-allowed" :
                          "text-muted-foreground hover:bg-white/5 hover:text-white",
              )}
            >
              <div className="flex items-start gap-2.5">
                <div className="mt-0.5 flex-shrink-0">
                  {done   ? <CheckCircle className="w-4 h-4 text-green-400" /> :
                   locked ? <Lock className="w-4 h-4 text-muted-foreground/30" /> :
                            <Circle className={cn("w-4 h-4", active ? "text-quantum-blue" : "text-muted-foreground/50")} />}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium truncate">{lesson.title}</p>
                  <p className="text-[10px] text-muted-foreground/60 mt-0.5">{lesson.estimated_minutes} min · {lesson.xp_reward} XP</p>
                </div>
              </div>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
'''

# ======================================================================
# FRONTEND: Hook for Learning
# ======================================================================

files[f"{FRONT}/src/hooks/useLearning.ts"] = '''
"use client";
import { useState, useEffect } from "react";
import { api } from "@/lib/api";

interface LessonMeta { id: string; title: string; order_index: number; xp_reward: number; estimated_minutes: number; }
interface Module { id: string; title: string; description: string; level: string; icon: string; lessons: LessonMeta[]; }

export function useLearning(moduleId?: string) {
  const [module, setModule] = useState<Module | null>(null);
  const [lessons, setLessons] = useState<(LessonMeta & { content?: string })[]>([]);
  const [completedIds, setCompletedIds] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!moduleId) return;
    (async () => {
      setLoading(true);
      try {
        const [modRes, progRes] = await Promise.all([
          api.get(`/learning/modules/${moduleId}`),
          api.get("/learning/progress"),
        ]);
        const mod = await modRes.json();
        const prog = await progRes.json();
        setModule(mod);
        setCompletedIds(prog.completed ?? []);

        // Pre-fetch all lessons
        const lessonData = await Promise.all(
          mod.lessons.map((l: LessonMeta) => api.get(`/learning/lessons/${l.id}`).then(r => r.json()))
        );
        setLessons(lessonData);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    })();
  }, [moduleId]);

  async function completeLesson(lessonId: string): Promise<number> {
    try {
      const res = await api.post(`/learning/lessons/${lessonId}/complete`);
      const data = await res.json();
      setCompletedIds(prev => [...new Set([...prev, lessonId])]);
      return data.xp_earned ?? 0;
    } catch {
      return 0;
    }
  }

  return { module, lessons, completedIds, completeLesson, loading };
}
'''

# ======================================================================
# FRONTEND: Gamification — Level-Up Modal
# ======================================================================

files[f"{FRONT}/src/components/gamification/LevelUpModal.tsx"] = '''
"use client";
import { motion, AnimatePresence } from "framer-motion";
import { Star, X } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";

interface LevelUpModalProps {
  visible: boolean;
  newLevel: number;
  onClose: () => void;
}

export function LevelUpModal({ visible, newLevel, onClose }: LevelUpModalProps) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
          <motion.div className="relative glass border border-quantum-blue/30 rounded-2xl p-10 max-w-sm w-full mx-4 text-center overflow-hidden"
            initial={{ scale: 0.7, y: 40 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.7, y: 40 }}
            transition={{ type: "spring", stiffness: 300, damping: 24 }}>

            {/* Background glow */}
            <div className="absolute inset-0 bg-quantum-blue/5 rounded-2xl" />

            {/* Stars animation */}
            {[...Array(6)].map((_, i) => (
              <motion.div key={i}
                className="absolute text-yellow-400"
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: [0, 1, 0], scale: [0, 1, 0], x: Math.cos(i * 60 * Math.PI / 180) * 80, y: Math.sin(i * 60 * Math.PI / 180) * 80 }}
                transition={{ delay: 0.3 + i * 0.1, duration: 1.2 }}
                style={{ left: "50%", top: "40%" }}
              >
                <Star className="w-5 h-5 fill-current" />
              </motion.div>
            ))}

            <button onClick={onClose} className="absolute top-4 right-4 text-muted-foreground hover:text-white">
              <X className="w-4 h-4" />
            </button>

            {/* Badge */}
            <motion.div
              className="w-24 h-24 rounded-full bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center mx-auto mb-6 shadow-[0_0_40px_rgba(0,212,255,0.4)]"
              initial={{ rotate: -180, scale: 0 }}
              animate={{ rotate: 0, scale: 1 }}
              transition={{ type: "spring", stiffness: 200, damping: 15 }}
            >
              <span className="text-4xl font-black text-quantum-dark">{newLevel}</span>
            </motion.div>

            <h2 className="text-2xl font-bold text-white mb-2">Level Up!</h2>
            <p className="text-muted-foreground mb-2">You\'ve reached</p>
            <p className="text-quantum-blue font-bold text-lg mb-6">Level {newLevel}</p>

            <GlowButton onClick={onClose} className="w-full justify-center">
              Keep Learning!
            </GlowButton>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
'''

# ======================================================================
# FRONTEND: Gamification — XP Progress Bar (animated)
# ======================================================================

files[f"{FRONT}/src/components/gamification/XPProgressBar.tsx"] = '''
import { motion } from "framer-motion";

interface XPProgressBarProps {
  xp: number;
  level: number;
  animated?: boolean;
}

const XP_PER_LEVEL = 500;

export function XPProgressBar({ xp, level, animated = true }: XPProgressBarProps) {
  const xpInLevel   = xp % XP_PER_LEVEL;
  const xpNeeded    = XP_PER_LEVEL;
  const percent     = Math.min((xpInLevel / xpNeeded) * 100, 100);

  return (
    <div className="w-full">
      <div className="flex justify-between text-xs text-muted-foreground mb-1.5">
        <span>Level {level}</span>
        <span>{xpInLevel} / {xpNeeded} XP</span>
      </div>
      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
        <motion.div
          className="h-full rounded-full bg-gradient-to-r from-quantum-blue to-quantum-purple"
          initial={animated ? { width: 0 } : { width: `${percent}%` }}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
        />
      </div>
      <div className="text-right text-[10px] text-muted-foreground/60 mt-1">
        {Math.round(xpNeeded - xpInLevel)} XP to Level {level + 1}
      </div>
    </div>
  );
}
'''

# ======================================================================
# FRONTEND: Gamification — Streak Tracker
# ======================================================================

files[f"{FRONT}/src/components/gamification/StreakTracker.tsx"] = '''
import { Flame } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface StreakTrackerProps {
  streak: number;
  className?: string;
}

const DAY_LABELS = ["M", "T", "W", "T", "F", "S", "S"];

export function StreakTracker({ streak, className }: StreakTrackerProps) {
  const today = new Date().getDay(); // 0 = Sunday
  const activeDays = Math.min(streak, 7);

  return (
    <div className={cn("glass rounded-xl border border-white/5 p-5", className)}>
      <div className="flex items-center gap-3 mb-5">
        <motion.div
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
        >
          <Flame className={cn("w-6 h-6", streak > 0 ? "text-orange-400" : "text-muted-foreground/30")} />
        </motion.div>
        <div>
          <p className="font-bold text-white">{streak} day{streak !== 1 ? "s" : ""}</p>
          <p className="text-xs text-muted-foreground">Current streak</p>
        </div>
      </div>

      <div className="flex gap-1.5 justify-between">
        {DAY_LABELS.map((label, i) => {
          const dayIndex = (i + 1) % 7; // Mon=1...Sun=0
          const isActive = activeDays >= (7 - ((today - dayIndex + 7) % 7));
          return (
            <div key={i} className="flex flex-col items-center gap-1.5">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: i * 0.05 }}
                className={cn(
                  "w-8 h-8 rounded-lg flex items-center justify-center text-sm",
                  isActive ? "bg-orange-500/20 border border-orange-500/40" : "bg-white/5 border border-white/5"
                )}
              >
                {isActive ? <Flame className="w-4 h-4 text-orange-400" /> : <div className="w-2 h-2 rounded-full bg-white/20" />}
              </motion.div>
              <span className="text-[10px] text-muted-foreground">{label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
'''

# ======================================================================
# FRONTEND: Gamification — Leaderboard
# ======================================================================

files[f"{FRONT}/src/app/leaderboard/page.tsx"] = '''
"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Trophy, Zap, Medal } from "lucide-react";
import { PageHeader } from "@/components/ui/PageHeader";
import { QuantumCard } from "@/components/ui/QuantumCard";

const MOCK_LEADERS = [
  { rank: 1,  name: "QuantumNova",    xp: 12450, level: 25, streak: 34, avatar: "QN" },
  { rank: 2,  name: "SchrodingerCat", xp: 11200, level: 23, streak: 21, avatar: "SC" },
  { rank: 3,  name: "WaveFunction",   xp:  9800, level: 20, streak: 15, avatar: "WF" },
  { rank: 4,  name: "QubitHero",      xp:  8400, level: 17, streak: 12, avatar: "QH" },
  { rank: 5,  name: "EntangleMaster", xp:  7100, level: 15, streak:  9, avatar: "EM" },
  { rank: 6,  name: "SuperpositionX", xp:  6200, level: 13, streak:  7, avatar: "SX" },
  { rank: 7,  name: "TeleportAce",    xp:  5400, level: 11, streak:  5, avatar: "TA" },
  { rank: 8,  name: "PhaseShifter",   xp:  4100, level:  9, streak:  3, avatar: "PS" },
  { rank: 9,  name: "OracleSeeker",   xp:  2800, level:  6, streak:  2, avatar: "OS" },
  { rank: 10, name: "You",            xp:  1200, level:  3, streak:  1, avatar: "ME", isMe: true },
];

const RANK_STYLES: Record<number, { icon: React.ReactNode; color: string }> = {
  1: { icon: <Trophy className="w-5 h-5 text-yellow-400 fill-yellow-400" />, color: "border-yellow-500/30 bg-yellow-500/5" },
  2: { icon: <Medal  className="w-5 h-5 text-gray-300 fill-gray-300" />,   color: "border-gray-400/30  bg-gray-400/5"  },
  3: { icon: <Medal  className="w-5 h-5 text-amber-600 fill-amber-600" />, color: "border-amber-600/30 bg-amber-600/5" },
};

const TABS = ["All Time", "This Week", "This Month"] as const;

export default function LeaderboardPage() {
  const [tab, setTab] = useState<typeof TABS[number]>("All Time");

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <PageHeader
        icon={<Trophy className="w-6 h-6 text-yellow-400" />}
        title="Leaderboard"
        subtitle="Top quantum learners this period"
      />

      {/* Tabs */}
      <div className="flex gap-1 mb-6 p-1 glass rounded-xl border border-white/5">
        {TABS.map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${
              tab === t ? "bg-quantum-blue/10 text-quantum-blue border border-quantum-blue/20" : "text-muted-foreground hover:text-white"
            }`}>
            {t}
          </button>
        ))}
      </div>

      {/* Top 3 podium */}
      <div className="flex items-end justify-center gap-4 mb-8">
        {[MOCK_LEADERS[1], MOCK_LEADERS[0], MOCK_LEADERS[2]].map((leader, i) => {
          const heights = ["h-24", "h-32", "h-20"];
          return (
            <motion.div key={leader.rank} initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
              transition={{ delay: i * 0.15 }} className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center text-quantum-dark font-bold">
                {leader.avatar}
              </div>
              <p className="text-xs text-white font-medium">{leader.name}</p>
              <p className="text-xs text-quantum-blue">{leader.xp.toLocaleString()} XP</p>
              <div className={`w-20 ${heights[i]} rounded-t-xl flex items-center justify-center ${
                i === 1 ? "bg-yellow-500/20 border border-yellow-500/30" :
                i === 0 ? "bg-gray-400/10 border border-gray-400/20" :
                           "bg-amber-700/10 border border-amber-700/20"
              }`}>
                <span className="text-2xl font-black text-muted-foreground/60">{leader.rank}</span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Full list */}
      <div className="space-y-2">
        {MOCK_LEADERS.map((leader, idx) => {
          const rankStyle = RANK_STYLES[leader.rank];
          return (
            <motion.div key={leader.rank}
              initial={{ x: -20, opacity: 0 }} animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.3 + idx * 0.04 }}
              className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${
                (leader as any).isMe
                  ? "border-quantum-blue/30 bg-quantum-blue/5"
                  : rankStyle ? rankStyle.color : "border-white/5 bg-white/2 hover:bg-white/5"
              }`}
            >
              <div className="w-8 text-center">
                {rankStyle ? rankStyle.icon : <span className="text-sm text-muted-foreground font-bold">{leader.rank}</span>}
              </div>
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-quantum-blue/30 to-quantum-purple/30 flex items-center justify-center text-sm font-bold text-white">
                {leader.avatar}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <p className="text-sm font-medium text-white">{leader.name}</p>
                  {(leader as any).isMe && <span className="text-xs text-quantum-blue font-medium">(you)</span>}
                </div>
                <p className="text-xs text-muted-foreground">Level {leader.level} · {leader.streak}d streak</p>
              </div>
              <div className="flex items-center gap-1 text-quantum-blue font-bold text-sm">
                <Zap className="w-3.5 h-3.5" />
                {leader.xp.toLocaleString()}
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
'''

# ======================================================================
# FRONTEND: Updated package.json (add new deps)
# ======================================================================

files[f"{FRONT}/package.json"] = '''{
  "name": "quantumverse-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "typescript": "5.5.3",
    "tailwindcss": "3.4.6",
    "framer-motion": "11.3.8",
    "lucide-react": "0.417.0",
    "recharts": "2.12.7",
    "react-markdown": "9.0.1",
    "remark-gfm": "4.0.0",
    "remark-math": "6.0.0",
    "rehype-katex": "7.0.1",
    "katex": "0.16.11",
    "react-syntax-highlighter": "15.5.0",
    "@types/react-syntax-highlighter": "15.5.13",
    "zustand": "4.5.4",
    "jose": "5.6.3",
    "clsx": "2.1.1",
    "tailwind-merge": "2.4.0",
    "class-variance-authority": "0.7.0",
    "@radix-ui/react-slot": "1.1.0",
    "@radix-ui/react-dialog": "1.1.1",
    "@radix-ui/react-tabs": "1.1.0",
    "@radix-ui/react-select": "2.1.1",
    "@radix-ui/react-tooltip": "1.1.2",
    "@radix-ui/react-progress": "1.1.0"
  },
  "devDependencies": {
    "@types/node": "22.0.0",
    "@types/react": "18.3.3",
    "@types/react-dom": "18.3.0",
    "autoprefixer": "10.4.19",
    "postcss": "8.4.40",
    "eslint": "8.57.0",
    "eslint-config-next": "14.2.5"
  }
}
'''

# ======================================================================
# BACKEND: requirements.txt (complete)
# ======================================================================

files[f"{BACK}/requirements.txt"] = '''fastapi==0.112.0
uvicorn[standard]==0.30.5
pydantic==2.8.2
pydantic-settings==2.4.0
sqlalchemy[asyncio]==2.0.31
asyncpg==0.29.0
alembic==1.13.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
httpx==0.27.0
qiskit==1.2.0
qiskit-aer==0.14.2
pytest==8.3.2
pytest-asyncio==0.23.8
anyio[trio]==4.4.0
python-dotenv==1.0.1
email-validator==2.2.0
python-multipart==0.0.9
'''

# Write all files
written = 0
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.lstrip('\n'))
    rel = path.replace('/data/quantumverse/', '')
    print(f"  {'FE' if 'frontend' in path else 'BE'}: {rel}")
    written += 1

print(f"\nPhase 5 total: {written} files")
