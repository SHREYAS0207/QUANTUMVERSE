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
} from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
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
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    level: 2,
    name: "Quantum Gates",
    short: "Gates & Circuits",
    description:
      "Learn the core gates that transform and control qubit states.",
    icon: Cpu,
    gradient: "from-purple-500 to-pink-500",
  },
  {
    level: 3,
    name: "Multi-Qubit Systems",
    short: "Entanglement",
    description:
      "Work with multiple qubits, controlled operations, and Bell states.",
    icon: GitBranch,
    gradient: "from-green-500 to-emerald-500",
  },
  {
    level: 4,
    name: "Quantum Algorithms",
    short: "Algorithms",
    description:
      "Explore the algorithms that demonstrate quantum computational advantage.",
    icon: Zap,
    gradient: "from-orange-500 to-yellow-500",
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
    () => modules.reduce((sum, m) => sum + (m.lesson_count || 0), 0),
    [modules]
  );

  const completedCount = progress.completed.length;

  const overallPercent = totalLessons
    ? Math.round((completedCount / totalLessons) * 100)
    : 0;

  if (loading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center h-64">
          <div className="w-8 h-8 border-2 border-quantum-blue/20 border-t-quantum-blue rounded-full animate-spin" />
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <PageHeader
        title="Learning Path"
        subtitle="Master quantum computing step by step"
      />

      <div className="glass rounded-2xl border border-white/5 p-5 mb-7">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-widest text-muted-foreground mb-1">
              Your journey
            </p>

            <h2 className="text-xl font-bold text-white">
              Quantum Computing Roadmap
            </h2>

            <p className="text-sm text-muted-foreground mt-1">
              Choose a level to open its dedicated lectures, activities, and
              progress.
            </p>
          </div>

          <div className="min-w-[220px]">
            <div className="flex items-center justify-between text-xs mb-2">
              <span className="text-muted-foreground">
                Overall progress
              </span>

              <span className="font-mono text-quantum-cyan">
                {completedCount}/{totalLessons || 0} lessons · {overallPercent}%
              </span>
            </div>

            <div className="h-2 rounded-full bg-white/5 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-quantum-blue to-quantum-cyan transition-all"
                style={{ width: `${overallPercent}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-6 rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-300">
          Learning data could not be loaded. Make sure the backend is running
          and the learning database is seeded.
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {LEVEL_META.map((meta, index) => {
          const levelModules = modules.filter(
            (m) => m.level === meta.level
          );

          const lessonCount = levelModules.reduce(
            (sum, m) => sum + (m.lesson_count || 0),
            0
          );

          const moduleTitle =
            levelModules[0]?.title || meta.name;

          const Icon = meta.icon;

          return (
            <motion.div
              key={meta.level}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.08 }}
            >
              <Link
                href={`/learn/level/${meta.level}`}
                className="block group"
              >
                <div className="glass rounded-2xl border border-white/5 hover:border-white/15 transition-all hover:-translate-y-1 overflow-hidden">
                  <div
                    className={`h-1.5 bg-gradient-to-r ${meta.gradient}`}
                  />

                  <div className="p-6">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-center gap-4">
                        <div
                          className={`w-12 h-12 rounded-xl bg-gradient-to-br ${meta.gradient} flex items-center justify-center`}
                        >
                          <Icon className="w-6 h-6 text-white" />
                        </div>

                        <div>
                          <p className="text-xs uppercase tracking-widest text-muted-foreground">
                            Level {meta.level} · {meta.short}
                          </p>

                          <h3 className="text-lg font-bold text-white group-hover:text-quantum-blue transition-colors mt-1">
                            {moduleTitle}
                          </h3>
                        </div>
                      </div>

                      <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:text-quantum-blue transition-colors mt-1" />
                    </div>

                    <p className="text-sm text-muted-foreground mt-4 leading-relaxed">
                      {levelModules[0]?.description || meta.description}
                    </p>

                    <div className="grid grid-cols-3 gap-2 mt-5">
                      <div className="rounded-lg bg-white/[0.03] border border-white/5 p-3 text-center">
                        <BookOpen className="w-4 h-4 mx-auto mb-1 text-quantum-cyan" />

                        <p className="text-xs text-muted-foreground">
                          Lectures
                        </p>

                        <p className="text-sm font-semibold text-white mt-0.5">
                          {lessonCount}
                        </p>
                      </div>

                      <div className="rounded-lg bg-white/[0.03] border border-white/5 p-3 text-center">
                        <Clock className="w-4 h-4 mx-auto mb-1 text-yellow-400" />

                        <p className="text-xs text-muted-foreground">
                          Level
                        </p>

                        <p className="text-sm font-semibold text-white mt-0.5">
                          {levelModules.length ? "Ready" : "Soon"}
                        </p>
                      </div>

                      <div className="rounded-lg bg-white/[0.03] border border-white/5 p-3 text-center">
                        <Trophy className="w-4 h-4 mx-auto mb-1 text-purple-400" />

                        <p className="text-xs text-muted-foreground">
                          Activities
                        </p>

                        <p className="text-sm font-semibold text-white mt-0.5">
                          Quiz + Lab
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center justify-between mt-5 pt-4 border-t border-white/5">
                      <span className="text-xs text-muted-foreground">
                        Open dedicated level workspace
                      </span>

                      <span className="text-xs font-semibold text-quantum-blue">
                        Continue →
                      </span>
                    </div>
                  </div>
                </div>
              </Link>
            </motion.div>
          );
        })}
      </div>

      {modules.length === 0 && !error && (
        <div className="glass rounded-xl border border-white/5 p-12 text-center mt-6">
          <BookOpen className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />

          <p className="text-muted-foreground">
            No learning modules are available yet.
          </p>
        </div>
      )}
    </AppShell>
  );
}
