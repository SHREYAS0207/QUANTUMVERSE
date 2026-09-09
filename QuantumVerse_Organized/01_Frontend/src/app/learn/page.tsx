"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, CheckCircle2, Lock, ChevronRight, Clock, Zap } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import api from "@/lib/api";
import type { LearningModule } from "@/types/learning";

const LEVEL_COLORS = ["from-blue-500 to-cyan-500", "from-purple-500 to-pink-500", "from-green-500 to-emerald-500", "from-orange-500 to-yellow-500"];
const LEVEL_ICONS = ["atom", "cpu", "link", "zap"];

export default function LearnPage() {
  const [modules, setModules] = useState<LearningModule[]>([]);
  const [progress, setProgress] = useState<{ completed: string[] }>({ completed: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/learning/modules").then((r) => r.data.modules),
      api.get("/learning/progress").then((r) => r.data).catch(() => ({ completed: [] })),
    ]).then(([mods, prog]) => {
      setModules(mods);
      setProgress(prog);
    }).finally(() => setLoading(false));
  }, []);

  const getModuleProgress = (module: LearningModule) => {
    if (!module.lesson_count) return 0;
    return 0; // Will be computed per lesson in detail view
  };

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
      <PageHeader title="Learning Path" subtitle="Master quantum computing step by step" />

      {/* Level progression */}
      <div className="flex items-center gap-2 mb-8 overflow-x-auto pb-2">
        {["Fundamentals", "Quantum Gates", "Multi-Qubit", "Algorithms"].map((lvl, i) => (
          <div key={lvl} className="flex items-center gap-2 flex-shrink-0">
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium bg-gradient-to-r ${LEVEL_COLORS[i]} text-white`}>
              <span>Level {i + 1}</span>
              <span className="opacity-80">{lvl}</span>
            </div>
            {i < 3 && <ChevronRight className="w-4 h-4 text-muted-foreground" />}
          </div>
        ))}
      </div>

      {/* Modules grid */}
      {modules.length === 0 ? (
        <div className="glass rounded-xl border border-white/5 p-12 text-center">
          <BookOpen className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
          <p className="text-muted-foreground">No modules found. Make sure the backend is running and seeded.</p>
          <p className="text-xs text-muted-foreground/60 mt-2">Run: <code className="font-mono bg-white/5 px-2 py-0.5 rounded">python -m app.database.seed</code></p>
        </div>
      ) : (
        <div className="space-y-6">
          {[1, 2, 3, 4].map((level) => {
            const levelModules = modules.filter((m) => m.level === level);
            if (!levelModules.length) return null;
            return (
              <div key={level}>
                <div className="flex items-center gap-3 mb-4">
                  <div className={`h-px flex-1 bg-gradient-to-r ${LEVEL_COLORS[level - 1]} opacity-30`} />
                  <span className={`text-xs font-semibold uppercase tracking-widest bg-gradient-to-r ${LEVEL_COLORS[level - 1]} bg-clip-text text-transparent`}>
                    Level {level}
                  </span>
                  <div className={`h-px flex-1 bg-gradient-to-l ${LEVEL_COLORS[level - 1]} opacity-30`} />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {levelModules.map((mod, i) => (
                    <motion.div
                      key={mod.id}
                      initial={{ opacity: 0, y: 15 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="glass rounded-xl border border-white/5 hover:border-quantum-blue/20 transition-all hover:-translate-y-1 p-5 cursor-pointer group"
                    >
                      <div className={`h-1 rounded-full bg-gradient-to-r ${LEVEL_COLORS[level - 1]} mb-4`} />
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="font-semibold text-white text-sm group-hover:text-quantum-blue transition-colors">{mod.title}</h3>
                          <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{mod.description}</p>
                        </div>
                        <ChevronRight className="w-4 h-4 text-muted-foreground/40 group-hover:text-quantum-blue transition-colors flex-shrink-0 ml-2" />
                      </div>
                      <div className="flex items-center gap-4 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <BookOpen className="w-3 h-3" /> {mod.lesson_count} lessons
                        </span>
                        <span className="flex items-center gap-1">
                          <Zap className="w-3 h-3 text-yellow-400" />
                          {mod.lesson_count * 50} XP
                        </span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </AppShell>
  );
}
