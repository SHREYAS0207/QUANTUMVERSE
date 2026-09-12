"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Atom,
  BookOpen,
  ChevronRight,
  Clock,
  Cpu,
  GitBranch,
  Trophy,
  Zap,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  Circle,
} from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import api from "@/lib/api";
import type { LearningModule, ProgressData } from "@/types/learning";

const LEVEL_META = [
  {
    level: 1,
    name: "Quantum Foundations",
    short: "Fundamentals",
    description:
      "Build the mental model you need before touching quantum circuits.",
    icon: Atom,
    gradient: "from-cyan-400 to-blue-500",
    glow: "bg-cyan-400/10",
  },
  {
    level: 2,
    name: "Quantum Gates",
    short: "Gates & Circuits",
    description:
      "Learn the core gates that transform and control qubit states.",
    icon: Cpu,
    gradient: "from-purple-400 to-pink-500",
    glow: "bg-purple-400/10",
  },
  {
    level: 3,
    name: "Multi-Qubit Systems",
    short: "Entanglement",
    description:
      "Work with multiple qubits, controlled operations, and Bell states.",
    icon: GitBranch,
    gradient: "from-emerald-400 to-green-500",
    glow: "bg-emerald-400/10",
  },
  {
    level: 4,
    name: "Quantum Algorithms",
    short: "Algorithms",
    description:
      "Explore algorithms that demonstrate quantum computational advantage.",
    icon: Zap,
    gradient: "from-orange-400 to-yellow-500",
    glow: "bg-orange-400/10",
  },
];

export default function LearnPage() {
  const [modules, setModules] = useState<LearningModule[]>([]);
  const [progress, setProgress] = useState<ProgressData>({
    completed: [],
    in_progress: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    Promise.all([
      api
        .get("/learning/modules")
        .then((r) => r.data.modules as LearningModule[]),

      api
        .get("/learning/progress")
        .then((r) => r.data as ProgressData)
        .catch(() => ({ completed: [], in_progress: [] })),
    ])
      .then(([mods, prog]) => {
        setModules(mods);
        setProgress(prog);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  const totalLessons = useMemo(
    () => modules.reduce((sum, module) => sum + (module.lesson_count || 0), 0),
    [modules]
  );

  const completedCount = progress.completed.length;

  const overallPercent = totalLessons
    ? Math.round((completedCount / totalLessons) * 100)
    : 0;

  const inProgressCount = progress.in_progress.length;

  if (loading) {
    return (
      <AppShell>
        <div className="flex min-h-[60vh] items-center justify-center">
          <div className="flex flex-col items-center gap-4">
            <div className="h-10 w-10 animate-spin rounded-full border-2 border-cyan-400/20 border-t-cyan-400" />
            <p className="text-xs text-white/35">
              Loading quantum curriculum...
            </p>
          </div>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      {/* Hero */}
      <section className="relative mb-8 overflow-hidden rounded-3xl border border-white/10 bg-white/[0.035] p-8 backdrop-blur-xl">
        <div className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-cyan-400/10 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-28 left-1/3 h-64 w-64 rounded-full bg-purple-500/10 blur-3xl" />

        <div className="relative flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
          <div className="max-w-2xl">
            <div className="mb-3 flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-cyan-300/70">
              <Sparkles className="h-4 w-4" />
              Quantum Academy
            </div>

            <h1 className="text-3xl font-bold tracking-tight text-white md:text-4xl">
              Master Quantum Computing
            </h1>

            <p className="mt-3 text-sm leading-6 text-white/45">
              Follow a structured path from quantum fundamentals to
              multi-qubit systems and advanced algorithms. Learn the theory,
              then experiment with it in the Quantum Lab.
            </p>

            <div className="mt-6 flex flex-wrap gap-3">
              <Link href="/learn/level/1">
                <button className="flex items-center gap-2 rounded-xl bg-cyan-400 px-5 py-2.5 text-sm font-bold text-black transition hover:bg-cyan-300">
                  Start Foundations
                  <ArrowRight className="h-4 w-4" />
                </button>
              </Link>

              <Link href="/quantum-lab">
                <button className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-white/10">
                  Open Quantum Lab
                </button>
              </Link>
            </div>
          </div>

          {/* Progress summary */}
          <div className="min-w-[280px] rounded-2xl border border-cyan-400/15 bg-black/30 p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[10px] uppercase tracking-[0.2em] text-white/30">
                  Overall Progress
                </p>
                <p className="mt-1 text-3xl font-bold text-white">
                  {overallPercent}%
                </p>
              </div>

              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-400/10">
                <Trophy className="h-6 w-6 text-cyan-300" />
              </div>
            </div>

            <div className="mt-5 h-2 overflow-hidden rounded-full bg-white/10">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${overallPercent}%` }}
                transition={{ duration: 1 }}
                className="h-full rounded-full bg-gradient-to-r from-cyan-400 to-blue-500"
              />
            </div>

            <div className="mt-3 flex items-center justify-between text-[10px]">
              <span className="text-white/35">
                {completedCount}/{totalLessons} lessons complete
              </span>

              <span className="text-cyan-300/70">
                {inProgressCount} in progress
              </span>
            </div>
          </div>
        </div>
      </section>

      {error && (
        <div className="mb-6 rounded-2xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-300">
          Learning data could not be loaded. Make sure the backend is running
          and the learning database is seeded.
        </div>
      )}

      {/* Roadmap heading */}
      <div className="mb-5 flex items-end justify-between">
        <div>
          <p className="text-[10px] uppercase tracking-[0.25em] text-cyan-300/50">
            Learning Roadmap
          </p>
          <h2 className="mt-1 text-xl font-bold text-white">
            Your Quantum Journey
          </h2>
        </div>

        <div className="hidden items-center gap-2 text-xs text-white/30 sm:flex">
          <BookOpen className="h-4 w-4" />
          {totalLessons} total lessons
        </div>
      </div>

      {/* Level cards */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        {LEVEL_META.map((meta, index) => {
          const levelModules = modules.filter(
            (module) => module.level === meta.level
          );

          const lessonCount = levelModules.reduce(
            (sum, module) => sum + (module.lesson_count || 0),
            0
          );

          const moduleTitle = levelModules[0]?.title || meta.name;
          const description =
            levelModules[0]?.description || meta.description;

          const Icon = meta.icon;

          const levelCompleted = progress.completed.filter((id) =>
            levelModules.some((module) => module.id === id)
          ).length;

          const levelPercent = lessonCount
            ? Math.round((levelCompleted / lessonCount) * 100)
            : 0;

          const available = levelModules.length > 0;

          return (
            <motion.div
              key={meta.level}
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.08 }}
            >
              <Link
                href={`/learn/level/${meta.level}`}
                className="group block"
              >
                <div className="relative overflow-hidden rounded-2xl border border-white/10 bg-white/[0.025] backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 hover:border-white/20 hover:bg-white/[0.045]">
                  {/* Gradient strip */}
                  <div
                    className={`h-1.5 bg-gradient-to-r ${meta.gradient}`}
                  />

                  {/* Glow */}
                  <div
                    className={`pointer-events-none absolute -right-20 -top-20 h-48 w-48 rounded-full ${meta.glow} blur-3xl opacity-0 transition-opacity duration-300 group-hover:opacity-100`}
                  />

                  <div className="relative p-6">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-center gap-4">
                        <div
                          className={`flex h-13 w-13 items-center justify-center rounded-xl bg-gradient-to-br ${meta.gradient}`}
                        >
                          <Icon className="h-6 w-6 text-white" />
                        </div>

                        <div>
                          <p className="text-[10px] uppercase tracking-[0.2em] text-white/30">
                            Level {meta.level} · {meta.short}
                          </p>

                          <h3 className="mt-1 text-lg font-bold text-white transition-colors group-hover:text-cyan-300">
                            {moduleTitle}
                          </h3>
                        </div>
                      </div>

                      <ChevronRight className="mt-1 h-5 w-5 text-white/20 transition-all group-hover:translate-x-1 group-hover:text-cyan-300" />
                    </div>

                    <p className="mt-5 text-sm leading-6 text-white/40">
                      {description}
                    </p>

                    {/* Progress */}
                    <div className="mt-5">
                      <div className="mb-2 flex items-center justify-between">
                        <span className="text-[10px] uppercase tracking-wider text-white/30">
                          Level progress
                        </span>

                        <span className="text-xs font-semibold text-cyan-300">
                          {levelPercent}%
                        </span>
                      </div>

                      <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${levelPercent}%` }}
                          transition={{
                            duration: 0.8,
                            delay: index * 0.08,
                          }}
                          className={`h-full rounded-full bg-gradient-to-r ${meta.gradient}`}
                        />
                      </div>
                    </div>

                    {/* Metadata */}
                    <div className="mt-5 grid grid-cols-3 gap-2">
                      <div className="rounded-xl border border-white/5 bg-white/[0.025] p-3 text-center">
                        <BookOpen className="mx-auto mb-1 h-4 w-4 text-cyan-300" />
                        <p className="text-[9px] uppercase tracking-wider text-white/25">
                          Lessons
                        </p>
                        <p className="mt-1 text-sm font-semibold text-white">
                          {lessonCount}
                        </p>
                      </div>

                      <div className="rounded-xl border border-white/5 bg-white/[0.025] p-3 text-center">
                        {levelCompleted === lessonCount && lessonCount > 0 ? (
                          <CheckCircle2 className="mx-auto mb-1 h-4 w-4 text-emerald-300" />
                        ) : (
                          <Circle className="mx-auto mb-1 h-4 w-4 text-white/30" />
                        )}

                        <p className="text-[9px] uppercase tracking-wider text-white/25">
                          Status
                        </p>

                        <p className="mt-1 text-xs font-semibold text-white">
                          {levelCompleted === lessonCount && lessonCount > 0
                            ? "Complete"
                            : available
                              ? "Available"
                              : "Soon"}
                        </p>
                      </div>

                      <div className="rounded-xl border border-white/5 bg-white/[0.025] p-3 text-center">
                        <Clock className="mx-auto mb-1 h-4 w-4 text-yellow-300" />
                        <p className="text-[9px] uppercase tracking-wider text-white/25">
                          Activities
                        </p>
                        <p className="mt-1 text-xs font-semibold text-white">
                          Quiz + Lab
                        </p>
                      </div>
                    </div>

                    {/* CTA */}
                    <div className="mt-5 flex items-center justify-between border-t border-white/5 pt-4">
                      <span className="text-xs text-white/25">
                        {levelPercent > 0
                          ? "Continue your progress"
                          : "Begin this level"}
                      </span>

                      <span className="flex items-center gap-1 text-xs font-semibold text-cyan-300">
                        Explore
                        <ArrowRight className="h-3 w-3" />
                      </span>
                    </div>
                  </div>
                </div>
              </Link>
            </motion.div>
          );
        })}
      </div>

      {/* Bottom learning tip */}
      <div className="mt-6 rounded-2xl border border-white/5 bg-white/[0.02] p-5">
        <div className="flex items-start gap-3">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-purple-400/10">
            <Atom className="h-4 w-4 text-purple-300" />
          </div>

          <div>
            <p className="text-xs font-semibold text-white">
              Learn by doing
            </p>
            <p className="mt-1 text-xs leading-5 text-white/30">
              After learning a concept, try it in the Quantum Lab. Building
              circuits and observing measurements is the fastest way to turn
              quantum theory into intuition.
            </p>
          </div>
        </div>
      </div>
    </AppShell>
  );
}