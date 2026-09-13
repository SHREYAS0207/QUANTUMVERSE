"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Atom,
  BookOpen,
  BrainCircuit,
  CheckCircle2,
  Flame,
  Gauge,
  Layers3,
  Sparkles,
  Target,
  Trophy,
  Zap,
} from "lucide-react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { useAuthStore } from "@/stores/authStore";

const modules = [
  {
    id: "superposition",
    title: "Superposition & Measurement",
    description: "Understand how qubits represent multiple states and how measurement collapses them.",
    level: "Beginner",
    minutes: 18,
    xp: 120,
    progress: 82,
    status: "In progress",
  },
  {
    id: "entanglement",
    title: "Entanglement & Bell States",
    description: "Explore non-classical correlations and the role of Bell states in teleportation.",
    level: "Intermediate",
    minutes: 22,
    xp: 150,
    progress: 54,
    status: "Continue",
  },
  {
    id: "gates",
    title: "Quantum Logic Gates",
    description: "See how common gates transform state vectors and probabilities in a circuit.",
    level: "Intermediate",
    minutes: 25,
    xp: 180,
    progress: 24,
    status: "New",
  },
  {
    id: "grover",
    title: "Grover's Search",
    description: "Learn amplitude amplification, oracle design, and the quadratic search speed-up.",
    level: "Advanced",
    minutes: 30,
    xp: 220,
    progress: 10,
    status: "Preview",
  },
];

const achievements = [
  { id: "speed-learner", title: "Speed Learner", desc: "Finish a lesson in under 5 minutes.", xp: 75, unlocked: true },
  { id: "circuit-builder", title: "Circuit Builder", desc: "Complete 5 quantum lab sessions.", xp: 100, unlocked: true },
  { id: "precision-solver", title: "Precision Solver", desc: "Score 90% or more on a problem set.", xp: 150, unlocked: false },
  { id: "teleportation-explorer", title: "Teleportation Explorer", desc: "Successfully explain teleportation in your own words.", xp: 180, unlocked: false },
];

const analytics = [
  { day: "Mon", minutes: 20 },
  { day: "Tue", minutes: 45 },
  { day: "Wed", minutes: 30 },
  { day: "Thu", minutes: 60 },
  { day: "Fri", minutes: 55 },
  { day: "Sat", minutes: 50 },
  { day: "Sun", minutes: 25 },
];

const quickActions = [
  { href: "/qlearn/ai-tutor", label: "Open AI Tutor", icon: BrainCircuit, color: "text-cyan-400" },
  { href: "/quantum-lab", label: "Build a Circuit", icon: Layers3, color: "text-violet-400" },
  { href: "/quantum-solver", label: "Solve a Problem", icon: Target, color: "text-emerald-400" },
  { href: "/quiz", label: "Take a Quiz", icon: Trophy, color: "text-yellow-400" },
];

const recommendedTopics = [
  "Bell state intuition",
  "Hadamard gate behavior",
  "Grover oracle design",
  "Quantum Fourier Transform",
];

export default function QLearnPage() {
  const { user } = useAuthStore();

  const stats = [
    { label: "Total XP", value: user?.xp ?? 420, icon: Zap, color: "text-yellow-400" },
    { label: "Lessons Done", value: user?.statistics?.total_lessons ?? 8, icon: BookOpen, color: "text-blue-400" },
    { label: "Circuits Built", value: user?.statistics?.total_circuits ?? 12, icon: Layers3, color: "text-purple-400" },
    { label: "Quiz Accuracy", value: `${user?.statistics?.quiz_accuracy ?? 86}%`, icon: Gauge, color: "text-green-400" },
  ];

  const unlockedAchievements = achievements.filter((a) => a.unlocked).length;

  return (
    <AppShell>
      <PageHeader
        title="Q-Learn AI"
        subtitle="Interactive quantum learning, guided practice, and progress tracking."
        icon={
          <div className="w-11 h-11 rounded-xl border border-quantum-blue/30 bg-quantum-blue/10 flex items-center justify-center">
            <Atom className="w-5 h-5 text-quantum-blue" />
          </div>
        }
      >
        <div className="flex items-center gap-2">
          <Link href="/qlearn/ai-tutor">
            <button className="inline-flex items-center gap-2 rounded-xl bg-quantum-blue px-4 py-2.5 text-sm font-semibold text-quantum-dark hover:opacity-90 transition-opacity">
              Open AI Tutor <ArrowRight className="w-4 h-4" />
            </button>
          </Link>
        </div>
      </PageHeader>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8 rounded-2xl border border-quantum-blue/20 bg-gradient-to-r from-quantum-blue/10 via-quantum-purple/10 to-cyan-500/10 p-6"
      >
        <div className="flex flex-col gap-5 xl:flex-row xl:items-center xl:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-quantum-blue/30 bg-quantum-blue/10 px-3 py-1.5 text-[10px] font-semibold uppercase tracking-[0.2em] text-quantum-blue">
              <Sparkles className="w-3.5 h-3.5" />
              QLearn Active
            </div>
            <h2 className="mt-4 text-2xl font-bold text-white">
              Learn quantum computing by doing, not just reading.
            </h2>
            <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
              Follow guided modules, solve real quantum problems, track learning analytics, and unlock achievements as you progress.
            </p>
          </div>

          <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-black/20 px-4 py-3 text-sm">
            <Flame className="w-5 h-5 text-orange-400" />
            <div>
              <div className="text-muted-foreground">Current streak</div>
              <div className="font-semibold text-white">{user?.streak_days ?? 7} day streak</div>
            </div>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((stat) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-xl border border-white/5 p-4"
          >
            <stat.icon className={`mb-3 w-6 h-6 ${stat.color}`} />
            <p className="text-2xl font-bold text-white">{stat.value}</p>
            <p className="mt-1 text-xs text-muted-foreground">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.6fr_1fr]">
        <div className="space-y-6">
          <section className="glass rounded-2xl border border-white/5 p-5">
            <div className="mb-4 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-quantum-blue" />
                <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Continue Learning</h3>
              </div>
              <Link href="/learn" className="text-xs text-quantum-blue hover:underline">
                Open all modules
              </Link>
            </div>

            <div className="space-y-3">
              {modules.map((module) => (
                <div key={module.id} className="rounded-xl border border-white/10 bg-white/5 p-4">
                  <div className="mb-2 flex items-center justify-between gap-3">
                    <div>
                      <h4 className="text-sm font-semibold text-white">{module.title}</h4>
                      <p className="mt-1 text-xs text-muted-foreground">{module.description}</p>
                    </div>
                    <span className="rounded-full border border-quantum-blue/30 bg-quantum-blue/10 px-2 py-1 text-[10px] font-medium uppercase tracking-[0.12em] text-quantum-blue">
                      {module.status}
                    </span>
                  </div>

                  <div className="mt-3 flex items-center justify-between text-[11px] text-muted-foreground">
                    <span>{module.level}</span>
                    <span>{module.minutes} min</span>
                    <span>{module.xp} XP</span>
                  </div>

                  <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/5">
                    <div className="h-full rounded-full bg-gradient-to-r from-quantum-blue to-quantum-purple" style={{ width: `${module.progress}%` }} />
                  </div>

                  <div className="mt-4 flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">{module.progress}% complete</span>
                    <Link href="/learn" className="text-xs font-medium text-quantum-blue hover:underline">
                      Resume lesson
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="glass rounded-2xl border border-white/5 p-5">
            <div className="mb-4 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Target className="w-4 h-4 text-quantum-purple" />
                <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Featured Modules</h3>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              {modules.map((module) => (
                <div key={`${module.id}-card`} className="rounded-2xl border border-white/10 bg-black/20 p-4">
                  <div className="mb-3 flex items-center justify-between">
                    <span className="rounded-full border border-white/10 bg-white/5 px-2 py-1 text-[10px] uppercase tracking-[0.14em] text-muted-foreground">
                      {module.level}
                    </span>
                    <span className="text-xs text-quantum-cyan">{module.xp} XP</span>
                  </div>
                  <h4 className="text-base font-semibold text-white">{module.title}</h4>
                  <p className="mt-2 text-sm text-muted-foreground">{module.description}</p>
                  <div className="mt-4 flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">{module.minutes} min lesson</span>
                    <Link href="/learn" className="inline-flex items-center gap-1 text-xs font-medium text-quantum-blue hover:underline">
                      Explore <ArrowRight className="w-3 h-3" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>

        <div className="space-y-6">
          <section className="glass rounded-2xl border border-white/5 p-5">
            <div className="mb-4 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Trophy className="w-4 h-4 text-yellow-400" />
                <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Recent Achievements</h3>
              </div>
              <Link href="/achievements" className="text-xs text-quantum-blue hover:underline">
                View all
              </Link>
            </div>

            <div className="space-y-3">
              {achievements.map((achievement) => (
                <div key={achievement.id} className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 p-3">
                  <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${achievement.unlocked ? "bg-gradient-to-br from-yellow-400 to-orange-500" : "bg-white/5"}`}>
                    {achievement.unlocked ? <CheckCircle2 className="w-5 h-5 text-white" /> : <Sparkles className="w-5 h-5 text-muted-foreground" />}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-white">{achievement.title}</p>
                    <p className="text-xs text-muted-foreground">{achievement.desc}</p>
                  </div>
                  <span className="text-[10px] uppercase tracking-[0.12em] text-quantum-cyan">{achievement.xp} XP</span>
                </div>
              ))}
            </div>

            <div className="mt-4 rounded-xl border border-quantum-blue/20 bg-quantum-blue/5 p-3 text-sm">
              <span className="font-semibold text-white">{unlockedAchievements}</span> / {achievements.length} achievements unlocked
            </div>
          </section>

          <section className="glass rounded-2xl border border-white/5 p-5">
            <div className="mb-4 flex items-center gap-2">
              <BrainCircuit className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Quick Actions</h3>
            </div>

            <div className="space-y-2">
              {quickActions.map(({ href, label, icon: Icon, color }) => (
                <Link key={href} href={href}>
                  <div className="flex items-center justify-between rounded-xl border border-white/10 bg-white/5 px-3 py-2.5 transition-colors hover:border-quantum-blue/30 hover:bg-quantum-blue/5">
                    <div className="flex items-center gap-3">
                      <Icon className={`w-4 h-4 ${color}`} />
                      <span className="text-sm text-white">{label}</span>
                    </div>
                    <ArrowRight className="w-3.5 h-3.5 text-muted-foreground" />
                  </div>
                </Link>
              ))}
            </div>
          </section>
        </div>
      </div>

      <div className="mt-8 grid gap-6 xl:grid-cols-[1.3fr_1fr]">
        <section className="glass rounded-2xl border border-white/5 p-5">
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Gauge className="w-4 h-4 text-emerald-400" />
              <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Learning Analytics</h3>
            </div>
            <Link href="/progress" className="text-xs text-quantum-blue hover:underline">
              Full progress view
            </Link>
          </div>

          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={analytics}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.12)" vertical={false} />
                <XAxis dataKey="day" tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis hide />
                <Tooltip
                  cursor={{ fill: "rgba(0, 212, 255, 0.06)" }}
                  contentStyle={{
                    backgroundColor: "#0D1F3C",
                    border: "1px solid rgba(0, 212, 255, 0.2)",
                    borderRadius: "8px",
                    color: "#e2e8f0",
                  }}
                />
                <Bar dataKey="minutes" fill="#00D4FF" radius={[6, 6, 0, 0]} opacity={0.85} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="glass rounded-2xl border border-white/5 p-5">
          <div className="mb-4 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-quantum-cyan" />
            <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Recommended Next</h3>
          </div>

          <div className="space-y-2">
            {recommendedTopics.map((topic) => (
              <div key={topic} className="rounded-xl border border-white/10 bg-white/5 px-3 py-2.5 text-sm text-muted-foreground">
                {topic}
              </div>
            ))}
          </div>
        </section>
      </div>
    </AppShell>
  );
}
