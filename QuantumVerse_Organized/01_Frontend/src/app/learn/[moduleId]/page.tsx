"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle,
  Clock,
  Zap,
  BookOpen,
  PanelLeft,
} from "lucide-react";

import { GlowButton } from "@/components/shared/GlowButton";
import { XPToast } from "@/components/shared/XPToast";
import { QuantumBadge } from "@/components/shared/QuantumBadge";
import { XPProgress } from "@/components/shared/XPProgress";
import { LessonContent } from "@/components/learn/LessonContent";
import { LessonSidebar } from "@/components/learn/LessonSidebar";
import { useLearning } from "@/hooks/useLearning";

export default function ModulePage() {
  const { moduleId } = useParams<{ moduleId: string }>();
  const router = useRouter();

  const {
    module,
    lessons,
    completedIds,
    completeLesson,
    loading,
  } = useLearning(moduleId);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [xp, setXp] = useState(0);
  const [showXP, setShowXP] = useState(false);
  const [completing, setCompleting] = useState(false);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black">
        <div className="flex flex-col items-center gap-4">
          <div className="h-10 w-10 animate-spin rounded-full border-2 border-cyan-400/20 border-t-cyan-400" />
          <p className="text-xs text-white/35">
            Loading quantum lesson...
          </p>
        </div>
      </div>
    );
  }

  if (!module) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black">
        <div className="rounded-2xl border border-red-400/15 bg-red-400/[0.05] px-6 py-5 text-sm text-red-300">
          Module not found.
        </div>
      </div>
    );
  }

  const currentLesson = lessons[currentIndex];
  const isCompleted = currentLesson
    ? completedIds.includes(currentLesson.id)
    : false;

  const completedCount = lessons.filter((lesson) =>
    completedIds.includes(lesson.id)
  ).length;

  const progressPercent = lessons.length
    ? Math.round((completedCount / lessons.length) * 100)
    : 0;

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
<div className="flex min-h-screen bg-black text-white">
  <div className="hidden lg:flex">
    <LessonSidebar
      module={module}
      lessons={lessons}
      currentIndex={currentIndex}
      completedIds={completedIds}
      onSelect={setCurrentIndex}
    />
  </div>

  <div className="flex min-w-0 flex-1 flex-col">
        {/* Top navigation */}
        <header className="sticky top-0 z-30 border-b border-white/[0.07] bg-black/75 backdrop-blur-xl">
          <div className="flex min-h-16 items-center justify-between gap-4 px-4 sm:px-6">
            <button
              onClick={() => router.push("/qlearn")}
              className="group flex items-center gap-2 rounded-lg px-2 py-2 text-sm text-white/40 transition-colors hover:bg-white/[0.04] hover:text-white"
            >
              <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-0.5" />
              <span className="hidden sm:inline">
                Back to modules
              </span>
            </button>

            <div className="flex items-center gap-2 sm:gap-4">
              {currentLesson && (
                <>
                  <div className="hidden items-center gap-1.5 text-xs text-white/35 sm:flex">
                    <Clock className="h-3.5 w-3.5" />
                    {currentLesson.estimated_minutes} min
                  </div>

                  <div className="flex items-center gap-1.5 text-xs text-cyan-300/70">
                    <Zap className="h-3.5 w-3.5" />
                    +{currentLesson.xp_reward} XP
                  </div>
                </>
              )}

              <div className="h-4 w-px bg-white/[0.08]" />

              <span className="text-xs font-medium tabular-nums text-white/40">
                {currentIndex + 1}
                <span className="mx-1 text-white/15">/</span>
                {lessons.length}
              </span>
            </div>
          </div>

          {/* Thin lesson progress */}
          <div className="h-px bg-white/[0.04]">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progressPercent}%` }}
              transition={{ duration: 0.5 }}
              className="h-full bg-gradient-to-r from-cyan-400 to-violet-400"
            />
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto">
          {currentLesson && (
            <motion.div
              key={currentLesson.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25 }}
              className="mx-auto w-full max-w-5xl px-4 py-7 sm:px-8 sm:py-10 lg:px-10 lg:py-12"
            >
              {/* Lesson context */}
              <div className="mb-8">
                <div className="mb-4 flex flex-wrap items-center gap-2">
                  <QuantumBadge variant="default" dot>
                    Lesson {currentIndex + 1}
                  </QuantumBadge>

                  {isCompleted && (
                    <QuantumBadge variant="success" dot>
                      Completed
                    </QuantumBadge>
                  )}
                </div>

                <div className="flex items-start gap-3">
                  <div className="mt-1 hidden h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-cyan-400/15 bg-cyan-400/[0.06] sm:flex">
                    <BookOpen className="h-5 w-5 text-cyan-300" />
                  </div>

                  <div>
                    <p className="qv-label text-cyan-400/50">
                      {module.title}
                    </p>

                    <h1 className="mt-1 text-2xl font-semibold tracking-tight text-white sm:text-3xl">
                      {currentLesson.title}
                    </h1>

                    <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-white/35">
                      <span className="flex items-center gap-1.5">
                        <Clock className="h-3.5 w-3.5" />
                        {currentLesson.estimated_minutes} minutes
                      </span>

                      <span className="h-3 w-px bg-white/[0.08]" />

                      <span className="flex items-center gap-1.5">
                        <Zap className="h-3.5 w-3.5 text-cyan-300" />
                        {currentLesson.xp_reward} XP reward
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Reading progress */}
              <div className="mb-8 rounded-2xl border border-white/[0.07] bg-white/[0.02] p-4">
                <XPProgress
                  current={completedCount}
                  target={Math.max(lessons.length, 1)}
                  label="MODULE PROGRESS"
                  showValues={false}
                  size="sm"
                />
              </div>

              {/* Lesson content */}
              <section className="relative overflow-hidden rounded-2xl border border-white/[0.07] bg-white/[0.02] p-5 shadow-[0_20px_70px_rgba(0,0,0,0.18)] sm:p-8 lg:p-10">
                <div
                  aria-hidden="true"
                  className="pointer-events-none absolute -right-24 -top-24 h-64 w-64 rounded-full bg-cyan-400/[0.035] blur-3xl"
                />

                <div className="relative">
                  <LessonContent
                    content={currentLesson.content ?? ""}
                  />
                </div>
              </section>

              {/* Navigation */}
              <div className="mt-8 flex flex-col gap-4 border-t border-white/[0.07] pt-6 sm:flex-row sm:items-center sm:justify-between">
                <GlowButton
                  variant="ghost"
                  disabled={currentIndex === 0}
                  onClick={() =>
                    setCurrentIndex((i) => i - 1)
                  }
                >
                  <ArrowLeft className="h-4 w-4" />
                  Previous
                </GlowButton>

                <div className="flex flex-wrap items-center justify-end gap-3">
                  {!isCompleted ? (
                    <GlowButton
                      onClick={handleComplete}
                      loading={completing}
                    >
                      <CheckCircle className="h-4 w-4" />
                      Mark Complete
                    </GlowButton>
                  ) : (
                    <div className="flex items-center gap-2 rounded-xl border border-emerald-400/15 bg-emerald-400/[0.05] px-4 py-2.5 text-sm font-medium text-emerald-300">
                      <CheckCircle className="h-4 w-4" />
                      Completed
                    </div>
                  )}

                  {currentIndex < lessons.length - 1 && (
                    <GlowButton
                      variant="secondary"
                      onClick={() =>
                        setCurrentIndex((i) => i + 1)
                      }
                    >
                      Next
                      <ArrowRight className="h-4 w-4" />
                    </GlowButton>
                  )}
                </div>
              </div>

              {/* Mobile curriculum hint */}
              <div className="mt-6 flex items-center justify-center gap-2 text-[11px] text-white/20 lg:hidden">
                <PanelLeft className="h-3.5 w-3.5" />
                Use the lesson navigation to move through the module.
              </div>
            </motion.div>
          )}
        </main>
      </div>

      <XPToast xp={xp} visible={showXP} />
    </div>
  );
}