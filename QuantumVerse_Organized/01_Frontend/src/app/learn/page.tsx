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
  FlaskConical,
} from "lucide-react";

import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { QuantumBadge } from "@/components/shared/QuantumBadge";
import { XPProgress } from "@/components/shared/XPProgress";
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
        .catch(() => ({
          completed: [],
          in_progress: [],
        })),
    ])
      .then(([mods, prog]) => {
        setModules(mods);
        setProgress(prog);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  const totalLessons = useMemo(
    () =>
      modules.reduce(
        (sum, module) => sum + (module.lesson_count || 0),
        0
      ),
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
      {/* Page header */}
      <PageHeader
        eyebrow="QLEARN // CURRICULUM"
        title="Master Quantum Computing"
        subtitle="Follow a structured path from quantum fundamentals to multi-qubit systems and advanced algorithms."
        icon={<Sparkles className="h-5 w-5" />}
        action={
          <div className="hidden items-center gap-2 sm:flex">
            <QuantumBadge variant="default" dot>
              {totalLessons} Lessons
            </QuantumBadge>

            <QuantumBadge variant="success" dot>
              {completedCount} Complete
            </QuantumBadge>
          </div>
        }
      />

      {/* Hero learning panel */}
      <section className="relative mb-8 overflow-hidden rounded-2xl border border-cyan-400/10 bg-cyan-400/[0.025] p-5 backdrop-blur-xl sm:p-6">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-cyan-400/[0.07] blur-3xl"
        />

        <div
          aria-hidden="true"
          className="pointer-events-none absolute -bottom-28 left-1/3 h-64 w-64 rounded-full bg-violet-500/[0.05] blur-3xl"
        />

        <div className="relative grid gap-6 lg:grid-cols-[1fr_320px] lg:items-center">
          <div>
            <div className="mb-4 flex items-center gap-2">
              <QuantumBadge variant="purple" dot>
                Quantum Academy
              </QuantumBadge>
            </div>

            <h2 className="max-w-2xl text-2xl font-semibold tracking-tight text-white sm:text-3xl">
              Build knowledge.
              <span className="qv-gradient-text"> Then build circuits.</span>
            </h2>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-white/40">
              Learn the theory, understand the mathematics, and immediately
              experiment with each concept inside the Quantum Lab.
            </p>

            <div className="mt-5 flex flex-wrap gap-3">
              <Link
                href="/learn/level/1"
                className="inline-flex items-center gap-2 rounded-xl border border-cyan-300/20 bg-cyan-400 px-5 py-2.5 text-sm font-semibold text-black shadow-[0_0_24px_rgba(0,212,255,0.15)] transition-all hover:bg-cyan-300 hover:shadow-[0_0_32px_rgba(0,212,255,0.22)]"
              >
                Start Foundations
                <ArrowRight className="h-4 w-4" />
              </Link>

              <Link
                href="/quantum-lab"
                className="inline-flex items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.03] px-5 py-2.5 text-sm font-medium text-white/70 transition-all hover:border-cyan-400/15 hover:bg-white/[0.06] hover:text-white"
              >
                <FlaskConical className="h-4 w-4" />
                Open Quantum Lab
              </Link>
            </div>
          </div>

          {/* Progress */}
          <QuantumCard className="p-5">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="qv-label text-cyan-400/60">
                  OVERALL PROGRESS
                </p>

                <p className="mt-2 text-3xl font-semibold tabular-nums text-white">
                  {overallPercent}%
                </p>
              </div>

              <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-400/15 bg-cyan-400/[0.07]">
                <Trophy className="h-5 w-5 text-cyan-300" />
              </div>
            </div>

            <div className="mt-5">
              <XPProgress
                current={completedCount}
                target={Math.max(totalLessons, 1)}
                label="CURRICULUM COMPLETION"
                showValues={false}
                size="md"
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
          </QuantumCard>
        </div>
      </section>

      {/* Error */}
      {error && (
        <div className="mb-6 flex items-start gap-3 rounded-2xl border border-red-400/15 bg-red-400/[0.05] p-4">
          <div className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-red-400" />

          <p className="text-sm leading-6 text-red-300">
            Learning data could not be loaded. Make sure the backend is
            running and the learning database is seeded.
          </p>
        </div>
      )}

      {/* Roadmap header */}
      <div className="mb-5 flex items-end justify-between gap-4">
        <div>
          <p className="qv-label text-cyan-400/60">
            LEARNING ROADMAP
          </p>

          <h2 className="mt-1 text-xl font-semibold tracking-tight text-white">
            Your Quantum Journey
          </h2>

          <p className="mt-1 text-sm text-white/35">
            Four stages from fundamentals to quantum algorithms.
          </p>
        </div>

        <div className="hidden items-center gap-2 rounded-full border border-white/[0.07] bg-white/[0.025] px-3 py-1.5 text-xs text-white/35 sm:flex">
          <BookOpen className="h-3.5 w-3.5" />
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

          const complete =
            levelCompleted === lessonCount && lessonCount > 0;

          return (
            <motion.div
              key={meta.level}
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                delay: index * 0.07,
                duration: 0.3,
              }}
            >
              <Link
                href={`/learn/level/${meta.level}`}
                className="group block"
              >
                <div className="relative overflow-hidden rounded-2xl border border-white/[0.08] bg-white/[0.025] backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 hover:border-white/[0.16] hover:bg-white/[0.045] hover:shadow-[0_18px_55px_rgba(0,0,0,0.25)]">
                  {/* Level accent */}
                  <div
                    className={`h-1 bg-gradient-to-r ${meta.gradient}`}
                  />

                  {/* Ambient glow */}
                  <div
                    className={`pointer-events-none absolute -right-20 -top-20 h-48 w-48 rounded-full ${meta.glow} blur-3xl opacity-0 transition-opacity duration-300 group-hover:opacity-100`}
                  />

                  <div className="relative p-5 sm:p-6">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex min-w-0 items-center gap-4">
                        <div
                          className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br ${meta.gradient} shadow-lg`}
                        >
                          <Icon className="h-5 w-5 text-white" />
                        </div>

                        <div className="min-w-0">
                          <div className="flex flex-wrap items-center gap-2">
                            <p className="qv-label">
                              Level {meta.level}
                            </p>

                            {complete && (
                              <QuantumBadge
                                variant="success"
                                dot
                              >
                                Complete
                              </QuantumBadge>
                            )}
                          </div>

                          <h3 className="mt-1 truncate text-lg font-semibold text-white transition-colors group-hover:text-cyan-300">
                            {moduleTitle}
                          </h3>
                        </div>
                      </div>

                      <ChevronRight className="mt-1 h-5 w-5 shrink-0 text-white/20 transition-all group-hover:translate-x-1 group-hover:text-cyan-300" />
                    </div>

                    <p className="mt-5 text-sm leading-6 text-white/40">
                      {description}
                    </p>

                    {/* Progress */}
                    <div className="mt-5">
                      <XPProgress
                        current={levelCompleted}
                        target={Math.max(lessonCount, 1)}
                        label="LEVEL PROGRESS"
                        showValues={false}
                        size="sm"
                      />
                    </div>

                    {/* Metadata */}
                    <div className="mt-5 grid grid-cols-3 gap-2">
                      <div className="rounded-xl border border-white/[0.06] bg-white/[0.025] p-3 text-center transition-colors group-hover:border-white/[0.09]">
                        <BookOpen className="mx-auto mb-1.5 h-4 w-4 text-cyan-300" />

                        <p className="qv-label">
                          Lessons
                        </p>

                        <p className="mt-1 text-sm font-semibold text-white">
                          {lessonCount}
                        </p>
                      </div>

                      <div className="rounded-xl border border-white/[0.06] bg-white/[0.025] p-3 text-center transition-colors group-hover:border-white/[0.09]">
                        {complete ? (
                          <CheckCircle2 className="mx-auto mb-1.5 h-4 w-4 text-emerald-300" />
                        ) : (
                          <Circle className="mx-auto mb-1.5 h-4 w-4 text-white/25" />
                        )}

                        <p className="qv-label">
                          Status
                        </p>

                        <p className="mt-1 text-xs font-semibold text-white">
                          {complete
                            ? "Complete"
                            : available
                              ? levelPercent > 0
                                ? "In Progress"
                                : "Available"
                              : "Soon"}
                        </p>
                      </div>

                      <div className="rounded-xl border border-white/[0.06] bg-white/[0.025] p-3 text-center transition-colors group-hover:border-white/[0.09]">
                        <Clock className="mx-auto mb-1.5 h-4 w-4 text-amber-300" />

                        <p className="qv-label">
                          Activities
                        </p>

                        <p className="mt-1 text-xs font-semibold text-white">
                          Quiz + Lab
                        </p>
                      </div>
                    </div>

                    {/* CTA */}
                    <div className="mt-5 flex items-center justify-between border-t border-white/[0.06] pt-4">
                      <span className="text-xs text-white/25">
                        {levelPercent > 0
                          ? "Continue your progress"
                          : available
                            ? "Begin this level"
                            : "Coming soon"}
                      </span>

                      <span className="flex items-center gap-1 text-xs font-semibold text-cyan-300 transition-transform group-hover:translate-x-0.5">
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

      {/* Learning tip */}
      <div className="mt-6 rounded-2xl border border-violet-400/10 bg-violet-400/[0.025] p-5 backdrop-blur-xl">
        <div className="flex items-start gap-3">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-violet-400/15 bg-violet-400/[0.07]">
            <Atom className="h-4 w-4 text-violet-300" />
          </div>

          <div>
            <p className="text-xs font-semibold text-white">
              Learn by doing
            </p>

            <p className="mt-1 text-xs leading-5 text-white/30">
              After learning a concept, try it in the Quantum Lab.
              Building circuits and observing measurements is the fastest
              way to turn quantum theory into intuition.
            </p>
          </div>
        </div>
      </div>
    </AppShell>
  );
}