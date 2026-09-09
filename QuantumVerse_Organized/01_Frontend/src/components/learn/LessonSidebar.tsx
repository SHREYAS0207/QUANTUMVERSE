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
