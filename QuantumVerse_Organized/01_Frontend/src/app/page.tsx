"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Atom, Zap, Bot, Trophy, FlaskConical, BookOpen, GitBranch, Cpu } from "lucide-react";

const FEATURES = [
  { icon: FlaskConical, title: "Drag-Drop Circuit Builder",     desc: "Build quantum circuits visually — no coding required." },
  { icon: Zap,          title: "Real-Time Qiskit Simulation",   desc: "Powered by IBM Qiskit Aer for accurate quantum results." },
  { icon: Bot,          title: "QubitAI Tutor",                  desc: "AI assistant that adapts explanations to your level." },
  { icon: BookOpen,     title: "Interactive Learning Paths",     desc: "From fundamentals to advanced algorithms, step by step." },
  { icon: GitBranch,    title: "Step-by-Step Execution",         desc: "Watch quantum state evolve gate by gate in real time." },
  { icon: Trophy,       title: "Gamified Progress",              desc: "Earn XP, badges, and track your quantum journey." },
];

const ALGORITHMS = [
  { name: "Grover's Search",   complexity: "O(√N)", color: "from-blue-500 to-cyan-500" },
  { name: "Quantum Teleportation", complexity: "3 qubits",  color: "from-purple-500 to-pink-500" },
  { name: "Deutsch-Jozsa",      complexity: "O(1) queries", color: "from-green-500 to-emerald-500" },
  { name: "Quantum Fourier Transform", complexity: "O(n²)",    color: "from-orange-500 to-yellow-500" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen text-white">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-quantum-blue/10">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Atom className="w-7 h-7 text-quantum-blue" />
            <span className="font-bold text-lg tracking-tight">QuantumVerse AI</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/login" className="text-sm text-muted-foreground hover:text-white transition-colors px-4 py-2">
              Sign In
            </Link>
            <Link href="/signup" className="text-sm px-4 py-2 rounded-lg bg-quantum-blue text-quantum-dark font-semibold hover:opacity-90 transition-opacity">
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-40 pb-24 px-6 text-center relative overflow-hidden">
        <div className="absolute inset-0 bg-glow-gradient pointer-events-none" />
        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-quantum-blue/30 bg-quantum-blue/5 text-quantum-blue text-sm font-mono mb-8">
            <span className="w-2 h-2 rounded-full bg-quantum-blue animate-pulse" />
            QuantumVerse AI
          </span>
          <h1 className="text-5xl md:text-7xl font-black tracking-tight mb-6">
            Learn Quantum Computing
            <br />
            <span className="bg-gradient-to-r from-quantum-blue via-quantum-purple to-quantum-cyan bg-clip-text text-transparent">
              by Experimenting
            </span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            Build quantum circuits visually, simulate with real Qiskit backend, learn from AI,
            and master quantum algorithms — no physics PhD required.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4">
            <Link href="/signup">
              <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}
                className="flex items-center gap-2 px-8 py-4 rounded-xl bg-quantum-blue text-quantum-dark font-bold text-lg hover:opacity-90 transition-all glow-blue">
                Start Learning <ArrowRight className="w-5 h-5" />
              </motion.button>
            </Link>
            <Link href="/quantum-lab">
              <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}
                className="flex items-center gap-2 px-8 py-4 rounded-xl border border-quantum-blue/30 text-white font-semibold text-lg hover:bg-quantum-blue/10 transition-all">
                <FlaskConical className="w-5 h-5" /> Explore Simulator
              </motion.button>
            </Link>
          </div>
        </motion.div>

        {/* Animated circuit preview */}
        <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4, duration: 0.8 }}
          className="mt-20 max-w-4xl mx-auto">
          <div className="glass rounded-2xl border border-quantum-blue/20 p-8 glow-blue">
            <div className="font-mono text-sm text-left space-y-4">
              {["|q0⟩", "|q1⟩", "|q2⟩"].map((q, i) => (
                <div key={q} className="flex items-center gap-3">
                  <span className="text-quantum-blue w-10">{q}</span>
                  <div className="flex-1 h-px bg-quantum-blue/20 relative">
                    {i === 0 && <div className="absolute left-[15%] -top-4 w-8 h-8 rounded-lg bg-cyan-500/20 border border-cyan-500/50 flex items-center justify-center text-xs text-cyan-400">H</div>}
                    {i === 0 && <div className="absolute left-[45%] -top-1 w-3 h-3 rounded-full bg-blue-400 border-2 border-blue-400" />}
                    {i === 1 && <div className="absolute left-[45%] -top-4 w-8 h-8 rounded-lg bg-purple-500/20 border border-purple-500/50 flex items-center justify-center text-xs text-purple-400">⊕</div>}
                    {i === 2 && <div className="absolute left-[70%] -top-4 w-8 h-8 rounded-lg bg-green-500/20 border border-green-500/50 flex items-center justify-center text-xs text-green-400">M</div>}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-6 flex items-center justify-between text-xs text-muted-foreground">
              <span>Bell State Circuit</span>
              <span className="text-quantum-cyan font-mono">|00⟩ → ½(|00⟩ + |11⟩)</span>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Features */}
      <section className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Everything You Need to Master Quantum Computing</h2>
          <p className="text-muted-foreground text-lg">One platform. Complete learning ecosystem.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((f, i) => (
            <motion.div key={f.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }} viewport={{ once: true }}
              className="glass rounded-xl p-6 border border-white/5 hover:border-quantum-blue/20 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 rounded-xl bg-quantum-blue/10 border border-quantum-blue/20 flex items-center justify-center mb-4">
                <f.icon className="w-6 h-6 text-quantum-blue" />
              </div>
              <h3 className="font-semibold text-white mb-2">{f.title}</h3>
              <p className="text-sm text-muted-foreground">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Algorithms */}
      <section className="py-24 px-6 bg-quantum-navy/30">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-4">Quantum Algorithm Explorer</h2>
          <p className="text-muted-foreground mb-12">Understand landmark quantum algorithms interactively.</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {ALGORITHMS.map((alg, i) => (
              <motion.div key={alg.name} initial={{ opacity: 0, scale: 0.9 }} whileInView={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }} viewport={{ once: true }}
                className="glass rounded-xl p-6 border border-white/5 hover:border-white/20 transition-all">
                <div className={`h-1 rounded-full bg-gradient-to-r ${alg.color} mb-4`} />
                <h3 className="font-semibold text-white mb-2 text-sm">{alg.name}</h3>
                <span className="font-mono text-xs text-muted-foreground">{alg.complexity}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { val: "4", label: "Learning Levels" },
            { val: "25+", label: "Lessons" },
            { val: "15+", label: "Quantum Gates" },
            { val: "4", label: "Famous Algorithms" },
          ].map((s) => (
            <div key={s.label}>
              <p className="text-4xl font-black text-quantum-blue">{s.val}</p>
              <p className="text-sm text-muted-foreground mt-1">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6 text-center">
        <div className="max-w-2xl mx-auto glass rounded-2xl border border-quantum-blue/20 p-12">
          <Atom className="w-12 h-12 text-quantum-blue mx-auto mb-6 animate-spin-slow" />
          <h2 className="text-3xl font-bold mb-4">Ready to Enter the Quantum Realm?</h2>
          <p className="text-muted-foreground mb-8">Join the future of computing education. Free for SIH demo.</p>
          <Link href="/signup">
            <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}
              className="px-10 py-4 rounded-xl bg-gradient-to-r from-quantum-blue to-quantum-purple text-white font-bold text-lg hover:opacity-90 transition-opacity">
              Start for Free
            </motion.button>
          </Link>
        </div>
      </section>

      <footer className="py-8 px-6 border-t border-white/5 text-center text-sm text-muted-foreground">
        <p>© 2024 QuantumVerse AI</p>
        <p className="mt-1 font-mono text-xs text-quantum-blue/50">Learn. Build. Simulate. Understand Quantum Computing.</p>
      </footer>
    </div>
  );
}
