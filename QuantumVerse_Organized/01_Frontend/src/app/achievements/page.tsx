"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Star, Lock, Zap } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import api from "@/lib/api";

const BADGE_COLORS: Record<string, string> = {
  blue: "from-blue-500 to-cyan-500",
  purple: "from-purple-500 to-pink-500",
  cyan: "from-cyan-500 to-emerald-500",
  gold: "from-yellow-400 to-orange-400",
  green: "from-green-500 to-emerald-400",
  orange: "from-orange-500 to-yellow-500",
  pink: "from-pink-500 to-rose-500",
};

export default function AchievementsPage() {
  const [achievements, setAchievements] = useState<any[]>([]);
  const [unlocked, setUnlocked] = useState<string[]>([]);

  useEffect(() => {
    Promise.all([
      api.get("/achievements").then((r) => r.data.achievements),
      api.get("/achievements/user").then((r) => r.data.unlocked.map((u: any) => u.achievement_id)).catch(() => []),
    ]).then(([achs, unlockedIds]) => {
      setAchievements(achs);
      setUnlocked(unlockedIds);
    });
  }, []);

  const unlockedCount = achievements.filter((a) => unlocked.includes(a.id)).length;

  return (
    <AppShell>
      <PageHeader title="Achievements" subtitle={`${unlockedCount} / ${achievements.length} unlocked`} />

      <div className="mb-6 glass rounded-xl border border-white/5 p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-muted-foreground">Overall Progress</span>
          <span className="text-sm font-mono text-quantum-blue">{unlockedCount}/{achievements.length}</span>
        </div>
        <div className="h-2 bg-muted rounded-full overflow-hidden">
          <motion.div
            animate={{ width: achievements.length ? `${(unlockedCount / achievements.length) * 100}%` : "0%" }}
            className="h-full bg-gradient-to-r from-quantum-blue to-quantum-cyan rounded-full"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {achievements.map((ach, i) => {
          const isUnlocked = unlocked.includes(ach.id);
          const gradient = BADGE_COLORS[ach.badge_color] ?? "from-slate-500 to-slate-600";
          return (
            <motion.div key={ach.id} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.05 }}
              className={`glass rounded-xl border p-5 text-center transition-all ${
                isUnlocked ? "border-quantum-blue/20 hover:border-quantum-blue/40" : "border-white/5 opacity-60"
              }`}>
              <div className={`w-16 h-16 rounded-2xl mx-auto mb-3 flex items-center justify-center bg-gradient-to-br ${gradient} ${
                isUnlocked ? "shadow-lg" : "grayscale opacity-50"
              }`}>
                {isUnlocked
                  ? <Star className="w-8 h-8 text-white" />
                  : <Lock className="w-8 h-8 text-white/60" />}
              </div>
              <h3 className="text-sm font-bold text-white mb-1">{ach.name}</h3>
              <p className="text-xs text-muted-foreground line-clamp-2 mb-2">{ach.description}</p>
              <div className="flex items-center justify-center gap-1 text-xs text-quantum-cyan">
                <Zap className="w-3 h-3" />
                <span>{ach.xp_reward} XP</span>
              </div>
              {isUnlocked && (
                <span className="mt-2 inline-block text-[10px] text-green-400 bg-green-400/10 border border-green-400/20 px-2 py-0.5 rounded-full">Unlocked ✓</span>
              )}
            </motion.div>
          );
        })}
      </div>
    </AppShell>
  );
}
