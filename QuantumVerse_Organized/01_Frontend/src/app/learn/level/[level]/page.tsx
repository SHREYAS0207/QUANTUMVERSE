"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  Clock,
  ExternalLink,
  FlaskConical,
  PlayCircle,
  Trophy,
  Zap,
} from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { QuantumCard } from "@/components/shared/QuantumCard";
import api from "@/lib/api";
import toast from "react-hot-toast";
import type {
  LearningModule,
  Lesson,
  ProgressData,
} from "@/types/learning";

const LEVEL_META: Record<
  number,
  {
    name: string;
    description: string;
    gradient: string;
    quizLabel: string;
  }
> = {
  1: {
    name: "Quantum Foundations",
    description:
      "Build the mental model behind qubits, states, superposition, and measurement.",
    gradient: "from-blue-500 to-cyan-500",
    quizLabel: "Foundations Quiz",
  },
  2: {
    name: "Quantum Gates",
    description:
      "Learn how quantum gates transform states and form the building blocks of circuits.",
    gradient: "from-purple-500 to-pink-500",
    quizLabel: "Gates Quiz",
  },
  3: {
    name: "Multi-Qubit Systems",
    description:
      "Explore controlled operations, entanglement, and Bell states.",
    gradient: "from-green-500 to-emerald-500",
    quizLabel: "Multi-Qubit Quiz",
  },
  4: {
    name: "Quantum Algorithms",
    description:
      "Study the major algorithms that demonstrate quantum computational advantage.",
    gradient: "from-orange-500 to-yellow-500",
    quizLabel: "Algorithms Quiz",
  },
};

export default function LevelPage() {
  const params = useParams<{ level: string }>();
  const router = useRouter();

  const level = Number(params.level);
  const meta = LEVEL_META[level];

  const [modules, setModules] = useState<LearningModule[]>([]);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [progress, setProgress] = useState<ProgressData>({
    completed: [],
    in_progress: [],
  });

  const [loading, setLoading] = useState(true);
  const [busyLesson, setBusyLesson] = useState<string | null>(null);

  useEffect(() => {
    if (!meta) {
      router.replace("/learn");
      return;
    }

    async function load() {
      try {
        const [moduleResponse, progressResponse] =
          await Promise.all([
            api.get("/learning/modules"),
            api
              .get("/learning/progress")
              .then((r) => r.data as ProgressData)
              .catch(() => ({
                completed: [],
                in_progress: [],
              })),
          ]);

        const levelModules = (
          moduleResponse.data.modules as LearningModule[]
        ).filter((m) => m.level === level);

        const details = await Promise.all(
          levelModules.map((m) =>
            api
              .get(`/learning/modules/${m.id}`)
              .then((r) => r.data)
          )
        );

        setModules(levelModules);

        setLessons(
          details.flatMap(
            (detail) => detail.lessons as Lesson[]
          )
        );

        setProgress(progressResponse);
      } catch {
        toast.error("Failed to load this learning level");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [level, meta, router]);

  const completedCount = useMemo(
    () =>
      lessons.filter((lesson) =>
        progress.completed.includes(lesson.id)
      ).length,
    [lessons, progress.completed]
  );

  const percent = lessons.length
    ? Math.round((completedCount / lessons.length) * 100)
    : 0;

  const totalXP = lessons.reduce(
    (sum, lesson) => sum + (lesson.xp_reward || 0),
    0
  );

  async function completeLesson(lesson: Lesson) {
    if (progress.completed.includes(lesson.id)) return;

    setBusyLesson(lesson.id);

    try {
      const { data } = await api.post(
        `/learning/lessons/${lesson.id}/complete`
      );

      setProgress((prev) => ({
        ...prev,
        completed: [...prev.completed, lesson.id],
      }));

      toast.success(
        `Lesson complete · +${data.xp_earned} XP`
      );
    } catch {
      toast.error("Could not mark the lesson complete");
    } finally {
      setBusyLesson(null);
    }
  }

  if (!meta) return null;

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
      <div className="mb-5">
        <button
          onClick={() => router.push("/learn")}
          className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-white transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Learning Path
        </button>
      </div>

      <div className="glass rounded-2xl border border-white/5 overflow-hidden mb-6">
        <div
          className={`h-2 bg-gradient-to-r ${meta.gradient}`}
        />

        <div className="p-6 md:p-8">
          <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                Level {level}
              </p>

              <h1 className="text-3xl font-bold text-white mt-2">
                {meta.name}
              </h1>

              <p className="text-sm text-muted-foreground mt-2 max-w-2xl">
                {modules[0]?.description || meta.description}
              </p>
            </div>

            <div className="flex flex-wrap gap-2">
              <Link
                href="/quiz"
                className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-quantum-blue text-quantum-dark text-sm font-bold hover:opacity-90 transition-opacity"
              >
                <Trophy className="w-4 h-4" />
                {meta.quizLabel}
              </Link>

              <Link
                href="/quantum-lab"
                className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl border border-white/10 text-white text-sm font-medium hover:border-white/20 transition-colors"
              >
                <FlaskConical className="w-4 h-4" />
                Practice in Lab
              </Link>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-7">
            <div className="rounded-xl bg-white/[0.03] border border-white/5 p-4">
              <p className="text-xs text-muted-foreground">
                Progress
              </p>
              <p className="text-xl font-bold text-white mt-1">
                {percent}%
              </p>
            </div>

            <div className="rounded-xl bg-white/[0.03] border border-white/5 p-4">
              <p className="text-xs text-muted-foreground">
                Lectures
              </p>
              <p className="text-xl font-bold text-white mt-1">
                {lessons.length}
              </p>
            </div>

            <div className="rounded-xl bg-white/[0.03] border border-white/5 p-4">
              <p className="text-xs text-muted-foreground">
                Completed
              </p>
              <p className="text-xl font-bold text-white mt-1">
                {completedCount}/{lessons.length}
              </p>
            </div>

            <div className="rounded-xl bg-white/[0.03] border border-white/5 p-4">
              <p className="text-xs text-muted-foreground">
                Available XP
              </p>
              <p className="text-xl font-bold text-white mt-1">
                {totalXP}
              </p>
            </div>
          </div>

          <div className="mt-5">
            <div className="h-2 rounded-full bg-white/5 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${percent}%` }}
                className={`h-full rounded-full bg-gradient-to-r ${meta.gradient}`}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-6">
        <div>
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-xs uppercase tracking-widest text-muted-foreground">
                Curriculum
              </p>

              <h2 className="text-lg font-bold text-white mt-1">
                Lectures & Lessons
              </h2>
            </div>

            <span className="text-xs text-muted-foreground">
              {completedCount} completed
            </span>
          </div>

          <div className="space-y-3">
            {lessons.map((lesson, index) => {
              const completed =
                progress.completed.includes(lesson.id);

              return (
                <motion.div
                  key={lesson.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.04 }}
                >
                  <QuantumCard className="p-4">
                    <div className="flex flex-col md:flex-row md:items-center gap-4">
                      <div
                        className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                          completed
                            ? "bg-green-500/10"
                            : "bg-white/5"
                        }`}
                      >
                        {completed ? (
                          <CheckCircle2 className="w-5 h-5 text-green-400" />
                        ) : (
                          <BookOpen className="w-5 h-5 text-quantum-cyan" />
                        )}
                      </div>

                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <span className="text-[11px] font-mono text-muted-foreground">
                            {String(index + 1).padStart(2, "0")}
                          </span>

                          <h3 className="text-sm font-semibold text-white">
                            {lesson.title}
                          </h3>
                        </div>

                        <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {lesson.estimated_minutes} min
                          </span>

                          <span className="flex items-center gap-1 text-yellow-400">
                            <Zap className="w-3 h-3" />
                            {lesson.xp_reward} XP
                          </span>

                          {completed && (
                            <span className="text-green-400">
                              Completed
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="flex gap-2">
                        <Link
                          href={`/learn/lesson/${lesson.id}?level=${level}`}
                          className="inline-flex items-center gap-2 px-3 py-2 rounded-lg border border-white/10 text-xs text-white hover:border-quantum-blue/40 transition-colors"
                        >
                          <PlayCircle className="w-3.5 h-3.5" />
                          Open Lecture
                        </Link>

                        <button
                          onClick={() => completeLesson(lesson)}
                          disabled={
                            completed ||
                            busyLesson === lesson.id
                          }
                          className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-xs text-muted-foreground hover:text-white disabled:opacity-50 transition-colors"
                        >
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          {busyLesson === lesson.id
                            ? "Saving..."
                            : completed
                            ? "Done"
                            : "Complete"}
                        </button>
                      </div>
                    </div>
                  </QuantumCard>
                </motion.div>
              );
            })}
          </div>
        </div>

        <div className="space-y-4">
          <QuantumCard>
            <p className="text-xs uppercase tracking-widest text-muted-foreground mb-3">
              Level actions
            </p>

            <div className="space-y-2">
              <Link
                href="/quiz"
                className="flex items-center justify-between p-3 rounded-xl border border-quantum-blue/20 bg-quantum-blue/5 hover:bg-quantum-blue/10 transition-colors"
              >
                <span className="flex items-center gap-2 text-sm text-white">
                  <Trophy className="w-4 h-4 text-yellow-400" />
                  Take quiz
                </span>

                <ExternalLink className="w-4 h-4 text-muted-foreground" />
              </Link>

              <Link
                href="/quantum-lab"
                className="flex items-center justify-between p-3 rounded-xl border border-white/10 hover:border-white/20 transition-colors"
              >
                <span className="flex items-center gap-2 text-sm text-white">
                  <FlaskConical className="w-4 h-4 text-quantum-cyan" />
                  Quantum Lab
                </span>

                <ExternalLink className="w-4 h-4 text-muted-foreground" />
              </Link>
            </div>
          </QuantumCard>

          <QuantumCard>
            <p className="text-xs uppercase tracking-widest text-muted-foreground mb-2">
              Recommended videos
            </p>

            <p className="text-sm text-muted-foreground leading-relaxed">
              Video resources can be attached to individual lessons once the
              curated YouTube links are added to the lesson data.
            </p>
          </QuantumCard>
        </div>
      </div>
    </AppShell>
  );
}
