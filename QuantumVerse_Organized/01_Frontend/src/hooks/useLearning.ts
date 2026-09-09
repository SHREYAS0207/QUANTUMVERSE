"use client";
import { useState, useEffect } from "react";
import { api } from "@/lib/api";

interface LessonMeta { id: string; title: string; order_index: number; xp_reward: number; estimated_minutes: number; }
interface Module { id: string; title: string; description: string; level: string; icon: string; lessons: LessonMeta[]; }

export function useLearning(moduleId?: string) {
  const [module, setModule] = useState<Module | null>(null);
  const [lessons, setLessons] = useState<(LessonMeta & { content?: string })[]>([]);
  const [completedIds, setCompletedIds] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!moduleId) return;
    (async () => {
      setLoading(true);
      try {
        const [modRes, progRes] = await Promise.all([
          api.get(`/learning/modules/${moduleId}`),
          api.get("/learning/progress"),
        ]);
        const mod = modRes.data;
        const prog = progRes.data;
        setModule(mod);
        setCompletedIds(prog.completed ?? []);

        // Pre-fetch all lessons
        const lessonData = await Promise.all(
          mod.lessons.map((l: LessonMeta) => api.get(`/learning/lessons/${l.id}`).then(r => r.data))
        );
        setLessons(lessonData);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    })();
  }, [moduleId]);

  async function completeLesson(lessonId: string): Promise<number> {
    try {
      const res = await api.post(`/learning/lessons/${lessonId}/complete`);
      const data = res.data;
      setCompletedIds(prev => [...new Set([...prev, lessonId])]);
      return data.xp_earned ?? 0;
    } catch {
      return 0;
    }
  }

  return { module, lessons, completedIds, completeLesson, loading };
}
