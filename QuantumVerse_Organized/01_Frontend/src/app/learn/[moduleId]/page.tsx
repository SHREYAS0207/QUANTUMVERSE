"use client";
import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { ArrowLeft, ArrowRight, CheckCircle, Clock, Zap } from "lucide-react";
import { GlowButton } from "@/components/shared/GlowButton";
import { XPToast } from "@/components/shared/XPToast";
import { LessonContent } from "@/components/learn/LessonContent";
import { LessonSidebar } from "@/components/learn/LessonSidebar";
import { useLearning } from "@/hooks/useLearning";

export default function ModulePage() {
  const { moduleId } = useParams<{ moduleId: string }>();
  const router = useRouter();
  const { module, lessons, completedIds, completeLesson, loading } = useLearning(moduleId);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [xp, setXp] = useState(0);
  const [showXP, setShowXP] = useState(false);
  const [completing, setCompleting] = useState(false);

  if (loading) return <div className="min-h-screen flex items-center justify-center text-muted-foreground">Loading module...</div>;
  if (!module) return <div className="min-h-screen flex items-center justify-center text-red-400">Module not found.</div>;

  const currentLesson = lessons[currentIndex];
  const isCompleted = currentLesson ? completedIds.includes(currentLesson.id) : false;

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
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <LessonSidebar
        module={module}
        lessons={lessons}
        currentIndex={currentIndex}
        completedIds={completedIds}
        onSelect={setCurrentIndex}
      />

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <div className="flex items-center justify-between p-4 border-b border-white/5 glass">
          <button onClick={() => router.push("/learn")} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" />
            Back to modules
          </button>
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            {currentLesson && (
              <>
                <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" />{currentLesson.estimated_minutes} min</span>
                <span className="flex items-center gap-1"><Zap className="w-3.5 h-3.5 text-quantum-blue" />+{currentLesson.xp_reward} XP</span>
              </>
            )}
            <span className="text-muted-foreground/50">{currentIndex + 1} / {lessons.length}</span>
          </div>
        </div>

        {/* Lesson */}
        <div className="flex-1 overflow-y-auto">
          {currentLesson && (
            <motion.div key={currentLesson.id} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.25 }}
              className="max-w-3xl mx-auto px-6 py-10">
              <LessonContent content={currentLesson.content ?? ""} />

              {/* Actions */}
              <div className="mt-10 flex items-center justify-between">
                <GlowButton variant="ghost" disabled={currentIndex === 0}
                  onClick={() => setCurrentIndex(i => i - 1)}>
                  <ArrowLeft className="w-4 h-4" /> Previous
                </GlowButton>

                <div className="flex gap-3">
                  {!isCompleted ? (
                    <GlowButton onClick={handleComplete} loading={completing}>
                      <CheckCircle className="w-4 h-4" /> Mark Complete
                    </GlowButton>
                  ) : (
                    <div className="flex items-center gap-2 text-green-400 text-sm font-medium">
                      <CheckCircle className="w-4 h-4" /> Completed!
                    </div>
                  )}

                  {currentIndex < lessons.length - 1 && (
                    <GlowButton variant="secondary" onClick={() => setCurrentIndex(i => i + 1)}>
                      Next <ArrowRight className="w-4 h-4" />
                    </GlowButton>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>

      <XPToast xp={xp} visible={showXP} />
    </div>
  );
}
