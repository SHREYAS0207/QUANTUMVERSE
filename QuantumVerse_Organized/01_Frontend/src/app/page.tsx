"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Atom, Zap, Bot, Trophy, FlaskConical, BookOpen, GitBranch, Activity, Orbit } from "lucide-react";

const FEATURES = [
  { icon: FlaskConical, title: "Drag-Drop Circuit Builder", desc: "Build quantum circuits visually — no coding required." },
  { icon: Zap, title: "Real-Time Qiskit Simulation", desc: "Powered by IBM Qiskit Aer for accurate quantum results." },
  { icon: Bot, title: "QubitAI Tutor", desc: "AI assistant that adapts explanations to your level." },
  { icon: BookOpen, title: "Interactive Learning Paths", desc: "From fundamentals to advanced algorithms, step by step." },
  { icon: GitBranch, title: "Step-by-Step Execution", desc: "Watch quantum state evolve gate by gate in real time." },
  { icon: Trophy, title: "Gamified Progress", desc: "Earn XP, badges, and track your quantum journey." },
];

const ALGORITHMS = [
  { name: "Grover's Search", complexity: "O(√N)" },
  { name: "Quantum Teleportation", complexity: "3 qubits" },
  { name: "Deutsch-Jozsa", complexity: "O(1) queries" },
  { name: "Quantum Fourier Transform", complexity: "O(n²)" },
];

function QuantumOrb() {
  return (
    <div className="relative mx-auto h-[310px] w-[310px] sm:h-[410px] sm:w-[410px]">
      <div className="absolute inset-[15%] rounded-full bg-cyan-300/[0.045] blur-3xl" />
      <div className="absolute inset-[10%] rounded-full border border-cyan-200/10 shadow-[0_0_70px_rgba(0,225,255,.08)]" />
      <div className="qv-orbit absolute inset-[17%] border-cyan-200/15" />
      <div className="qv-orbit absolute inset-[7%] border-purple-300/10" style={{ animationDuration: "22s", animationDirection: "reverse" }} />
      <div className="absolute inset-[27%] rounded-full border border-dashed border-white/[0.08]" />
      <div className="absolute left-1/2 top-1/2 h-20 w-20 -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-200/25 bg-cyan-200/[0.07] shadow-[0_0_45px_rgba(0,225,255,.18)]">
        <div className="absolute inset-3 rounded-full border border-white/[0.08] bg-[#071016]" />
        <Atom className="absolute inset-0 m-auto h-8 w-8 text-cyan-200" />
      </div>
      {[
        ["left-[20%] top-[34%]", "bg-cyan-200"],
        ["right-[17%] top-[27%]", "bg-violet-300"],
        ["right-[25%] bottom-[20%]", "bg-emerald-200"],
        ["left-[24%] bottom-[24%]", "bg-white"],
      ].map(([pos, dot], i) => (
        <motion.span
          key={i}
          className={`absolute ${pos} h-2.5 w-2.5 rounded-full ${dot} shadow-[0_0_16px_currentColor]`}
          animate={{ scale: [1, 1.55, 1], opacity: [.65, 1, .65] }}
          transition={{ duration: 2.2 + i * .35, repeat: Infinity, ease: "easeInOut" }}
        />
      ))}
    </div>
  );
}

export default function LandingPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[#030507] text-white">
      <nav className="fixed top-0 z-50 w-full border-b border-white/[0.07] bg-[#030507]/65 backdrop-blur-2xl">
        <div className="mx-auto flex h-[72px] max-w-7xl items-center justify-between px-5 sm:px-8">
          <Link href="/" className="group flex items-center gap-3">
            <div className="relative flex h-9 w-9 items-center justify-center rounded-xl border border-cyan-300/25 bg-cyan-300/[0.055]">
              <Atom className="h-5 w-5 text-cyan-200 transition-transform duration-700 group-hover:rotate-180" />
            </div>
            <div>
              <div className="text-sm font-semibold tracking-[0.19em]">QUANTUM<span className="text-cyan-300">VERSE</span></div>
              <div className="font-mono text-[8px] uppercase tracking-[0.24em] text-white/25">Learn · Build · Simulate</div>
            </div>
          </Link>
          <div className="flex items-center gap-2">
            <Link href="/login" className="rounded-lg px-4 py-2 text-xs text-white/55 transition-colors hover:bg-white/[0.035] hover:text-white">Sign In</Link>
            <Link href="/signup" className="rounded-lg border border-cyan-200/25 bg-cyan-200/[0.09] px-4 py-2 text-xs font-semibold text-cyan-100 shadow-[0_0_24px_rgba(0,225,255,.08)] transition-all hover:bg-cyan-200/[0.14]">Get Started</Link>
          </div>
        </div>
      </nav>

      <main>
        <section className="relative min-h-screen px-5 pb-20 pt-32 sm:px-8 lg:pt-40">
          <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_70%_50%_at_50%_0%,rgba(0,226,255,.11),transparent_68%)]" />
          <div className="relative mx-auto grid max-w-7xl items-center gap-10 lg:grid-cols-[1.05fr_.95fr]">
            <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .75 }}>
              <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-cyan-200/15 bg-cyan-200/[0.045] px-3 py-1.5 font-mono text-[9px] uppercase tracking-[0.2em] text-cyan-200/75">
                <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-cyan-200 shadow-[0_0_10px_rgba(0,225,255,.9)]" />
                Quantum Research Environment · QV-01
              </div>
              <h1 className="max-w-4xl text-5xl font-black leading-[.98] tracking-[-.045em] sm:text-6xl lg:text-7xl xl:text-[82px]">
                Learn Quantum Computing
                <span className="block pt-2 qv-gradient-text">by experimenting.</span>
              </h1>
              <p className="mt-7 max-w-2xl text-base leading-7 text-white/45 sm:text-lg">
                Build quantum circuits visually, simulate with real Qiskit backend, learn from AI, and master quantum algorithms — no physics PhD required.
              </p>
              <div className="mt-9 flex flex-wrap gap-3">
                <Link href="/signup">
                  <motion.button whileHover={{ y: -2 }} whileTap={{ scale: .98 }} className="flex items-center gap-2 rounded-xl border border-cyan-200/30 bg-cyan-200/[0.1] px-6 py-3.5 text-sm font-bold text-cyan-50 shadow-[0_0_32px_rgba(0,225,255,.1)]">
                    Start Learning <ArrowRight className="h-4 w-4" />
                  </motion.button>
                </Link>
                <Link href="/quantum-lab">
                  <motion.button whileHover={{ y: -2 }} whileTap={{ scale: .98 }} className="flex items-center gap-2 rounded-xl border border-white/[0.09] bg-white/[0.025] px-6 py-3.5 text-sm font-semibold text-white/80 hover:bg-white/[0.05]">
                    <FlaskConical className="h-4 w-4 text-cyan-200" /> Explore Simulator
                  </motion.button>
                </Link>
              </div>
              <div className="mt-12 grid max-w-xl grid-cols-3 gap-4 border-t border-white/[0.07] pt-5">
                {[
                  ["04", "Learning levels"],
                  ["25+", "Interactive lessons"],
                  ["15+", "Quantum gates"],
                ].map(([v, l]) => (
                  <div key={l}>
                    <div className="font-mono text-lg text-cyan-200">{v}</div>
                    <div className="mt-1 text-[9px] uppercase tracking-[0.15em] text-white/25">{l}</div>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div initial={{ opacity: 0, scale: .92 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: .18, duration: .9 }} className="relative">
              <QuantumOrb />
              <div className="absolute bottom-0 left-1/2 w-[90%] -translate-x-1/2 rounded-2xl border border-white/[0.08] bg-[#060b10]/75 p-4 backdrop-blur-xl">
                <div className="flex items-center justify-between">
                  <span className="qv-label">Live state preview</span>
                  <span className="flex items-center gap-1.5 font-mono text-[9px] text-emerald-300"><Activity className="h-3 w-3" /> STABLE</span>
                </div>
                <div className="mt-3 grid grid-cols-3 gap-2 font-mono text-[10px]">
                  <div className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-2"><span className="text-white/25">STATE</span><div className="mt-1 text-cyan-200">|ψ⟩</div></div>
                  <div className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-2"><span className="text-white/25">PHASE</span><div className="mt-1 text-violet-200">π / 2</div></div>
                  <div className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-2"><span className="text-white/25">FIDELITY</span><div className="mt-1 text-emerald-200">99.8%</div></div>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        <section className="relative border-y border-white/[0.06] bg-white/[0.012] px-5 py-24 sm:px-8">
          <div className="mx-auto max-w-7xl">
            <div className="mb-12 max-w-2xl">
              <div className="qv-label mb-3">Research instruments</div>
              <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">Everything you need to master quantum computing.</h2>
              <p className="mt-3 text-sm leading-6 text-white/40">One platform. A complete learning and experimentation environment.</p>
            </div>
            <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
              {FEATURES.map((f, i) => (
                <motion.div key={f.title} initial={{ opacity: 0, y: 18 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: i * .06 }} viewport={{ once: true }} className="qv-panel group rounded-2xl p-5 transition-transform duration-300 hover:-translate-y-1">
                  <div className="mb-8 flex items-center justify-between">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-200/15 bg-cyan-200/[0.045]">
                      <f.icon className="h-5 w-5 text-cyan-200" />
                    </div>
                    <span className="font-mono text-[9px] text-white/15">0{i + 1}</span>
                  </div>
                  <h3 className="text-sm font-semibold text-white/90">{f.title}</h3>
                  <p className="mt-2 text-xs leading-5 text-white/35">{f.desc}</p>
                  <div className="mt-5 h-px bg-gradient-to-r from-cyan-200/20 to-transparent" />
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <section className="px-5 py-24 sm:px-8">
          <div className="mx-auto max-w-7xl">
            <div className="mb-10 flex items-end justify-between gap-4">
              <div>
                <div className="qv-label mb-3">Algorithm observatory</div>
                <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">Explore landmark algorithms.</h2>
              </div>
              <Orbit className="hidden h-9 w-9 text-cyan-200/30 sm:block" />
            </div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {ALGORITHMS.map((alg, i) => (
                <motion.div key={alg.name} whileHover={{ y: -3 }} className="qv-panel rounded-2xl p-5">
                  <div className="mb-8 flex items-center justify-between">
                    <span className="font-mono text-[9px] text-cyan-200/50">ALGORITHM / 0{i + 1}</span>
                    <div className="h-1.5 w-1.5 rounded-full bg-cyan-200 shadow-[0_0_9px_rgba(0,225,255,.8)]" />
                  </div>
                  <h3 className="min-h-[42px] text-sm font-semibold text-white/85">{alg.name}</h3>
                  <div className="mt-4 font-mono text-xs text-white/30">{alg.complexity}</div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <section className="px-5 pb-28 pt-4 sm:px-8">
          <div className="mx-auto max-w-4xl overflow-hidden rounded-3xl border border-cyan-200/12 bg-gradient-to-br from-cyan-200/[0.06] via-white/[0.015] to-violet-300/[0.04] p-8 text-center sm:p-12">
            <div className="mx-auto mb-6 flex h-14 w-14 items-center justify-center rounded-full border border-cyan-200/20 bg-cyan-200/[0.06]">
              <Atom className="h-7 w-7 text-cyan-200" />
            </div>
            <div className="qv-label mb-3">Initialize your workspace</div>
            <h2 className="text-3xl font-bold tracking-tight">Ready to enter the quantum realm?</h2>
            <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-white/38">Join the future of computing education. Free for SIH demo.</p>
            <Link href="/signup">
              <motion.button whileHover={{ y: -2 }} whileTap={{ scale: .98 }} className="mt-8 rounded-xl border border-cyan-200/25 bg-cyan-200/[0.09] px-8 py-3.5 text-sm font-bold text-cyan-50 shadow-[0_0_30px_rgba(0,225,255,.08)]">
                Start for Free
              </motion.button>
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t border-white/[0.06] px-5 py-8 text-center sm:px-8">
        <p className="text-[11px] text-white/25">© 2024 QuantumVerse AI</p>
        <p className="mt-1 font-mono text-[9px] uppercase tracking-[0.18em] text-cyan-200/20">Learn · Build · Simulate · Understand Quantum Computing</p>
      </footer>
    </div>
  );
}
