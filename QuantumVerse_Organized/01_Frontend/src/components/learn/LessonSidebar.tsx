"use client";

import {
  CheckCircle,
  Circle,
  Lock,
  BookOpen,
  Clock,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Lesson {
  id: string;
  title: string;
  estimated_minutes: number;
  xp_reward: number;
}

interface Module {
  title: string;
  level: string;
}

interface LessonSidebarProps {
  module: Module;
  lessons: Lesson[];
  currentIndex: number;
  completedIds: string[];
  onSelect: (i: number) => void;
}

const LEVEL_STYLES: Record<string, string> = {
  beginner: "border-emerald-400/15 bg-emerald-400/[0.07] text-emerald-300",
  intermediate: "border-amber-400/15 bg-amber-400/[0.07] text-amber-300",
  advanced: "border-red-400/15 bg-red-400/[0.07] text-red-300",
};

export function LessonSidebar({
  module,
  lessons,
  currentIndex,
  completedIds,
  onSelect,
}: LessonSidebarProps) {
  const completedCount = completedIds.length;

  const progress = lessons.length
    ? Math.round((completedCount / lessons.length) * 100)
    : 0;

  return (
    <aside className="flex w-72 shrink-0 flex-col overflow-y-auto border-r border-white/[0.07] bg-black/60 backdrop-blur-xl">
      {/* Module identity */}
      <div className="border-b border-white/[0.07] p-5">
        <div className="mb-4 flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-cyan-400/15 bg-cyan-400/[0.07]">
            <BookOpen className="h-4 w-4 text-cyan-300" />
          </div>

          <span className="qv-label text-cyan-400/55">
            QLEARN
          </span>
        </div>

        <h2 className="text-sm font-semibold leading-5 text-white">
          {module.title}
        </h2>

        <span
          className={cn(
            "mt-3 inline-flex rounded-full border px-2.5 py-1",
            "text-[10px] font-semibold uppercase tracking-[0.08em]",
            LEVEL_STYLES[module.level] ??
              "border-cyan-400/15 bg-cyan-400/[0.07] text-cyan-300"
          )}
        >
          {module.level}
        </span>
      </div>

      {/* Progress */}
      <div className="border-b border-white/[0.05] px-5 py-4">
        <div className="mb-2 flex items-center justify-between">
          <span className="qv-label">MODULE PROGRESS</span>

          <span className="text-xs font-medium tabular-nums text-white/45">
            {progress}%
          </span>
        </div>

        <div className="h-1.5 overflow-hidden rounded-full bg-white/[0.06]">
          <div
            className="h-full rounded-full bg-gradient-to-r from-cyan-400 to-violet-400 transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>

        <div className="mt-2 flex items-center justify-between text-[10px] text-white/25">
          <span>
            {completedCount} of {lessons.length} complete
          </span>

          <span>
            {lessons.length - completedCount} remaining
          </span>
        </div>
      </div>

      {/* Lesson list */}
      <nav className="flex-1 p-3">
        <p className="qv-label mb-2 px-2 text-white/25">
          LESSONS
        </p>

        <div className="space-y-1">
          {lessons.map((lesson, i) => {
            const done = completedIds.includes(lesson.id);
            const active = i === currentIndex;

            const locked =
              i > 0 &&
              !completedIds.includes(lessons[i - 1].id) &&
              !done;

            return (
              <button
                key={lesson.id}
                onClick={() => !locked && onSelect(i)}
                disabled={locked}
                className={cn(
                  "group relative w-full rounded-xl border px-3 py-3 text-left",
                  "transition-all duration-200",
                  active
                    ? "border-cyan-400/20 bg-cyan-400/[0.07] shadow-[inset_2px_0_0_rgba(0,212,255,0.75)]"
                    : done
                      ? "border-transparent hover:border-white/[0.06] hover:bg-white/[0.035]"
                      : locked
                        ? "cursor-not-allowed border-transparent opacity-45"
                        : "border-transparent hover:border-white/[0.06] hover:bg-white/[0.035]"
                )}
              >
                <div className="flex items-start gap-3">
                  {/* Status */}
                  <div className="mt-0.5 shrink-0">
                    {done ? (
                      <CheckCircle className="h-4 w-4 text-emerald-300" />
                    ) : locked ? (
                      <Lock className="h-4 w-4 text-white/20" />
                    ) : (
                      <Circle
                        className={cn(
                          "h-4 w-4",
                          active
                            ? "text-cyan-300"
                            : "text-white/25"
                        )}
                      />
                    )}
                  </div>

                  {/* Content */}
                  <div className="min-w-0 flex-1">
                    <p
                      className={cn(
                        "truncate text-xs font-medium",
                        active
                          ? "text-white"
                          : done
                            ? "text-white/60"
                            : "text-white/45"
                      )}
                    >
                      {lesson.title}
                    </p>

                    <div className="mt-1.5 flex items-center gap-2 text-[10px] text-white/25">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {lesson.estimated_minutes} min
                      </span>

                      <span className="text-white/10">•</span>

                      <span className="flex items-center gap-1">
                        <Zap className="h-3 w-3 text-cyan-400/50" />
                        {lesson.xp_reward} XP
                      </span>
                    </div>
                  </div>

                  {/* Lesson number */}
                  <span
                    className={cn(
                      "text-[9px] font-medium tabular-nums",
                      active
                        ? "text-cyan-300/60"
                        : "text-white/15"
                    )}
                  >
                    {String(i + 1).padStart(2, "0")}
                  </span>
                </div>
              </button>
            );
          })}
        </div>
      </nav>

      {/* Sidebar footer */}
      <div className="border-t border-white/[0.06] p-4">
        <div className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-3">
          <div className="flex items-center gap-2">
            <div className="h-1.5 w-1.5 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(0,212,255,0.7)]" />

            <span className="text-[10px] font-medium uppercase tracking-[0.1em] text-white/35">
              Learning mode
            </span>
          </div>

          <p className="mt-2 text-[10px] leading-4 text-white/20">
            Complete lessons sequentially to unlock the next concept.
          </p>
        </div>
      </div>
    </aside>
  );
}