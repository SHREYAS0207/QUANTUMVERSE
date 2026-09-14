"use client";

import { CheckCircle2, Sparkles, Trophy } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";

const achievements = [
  {
    id: "speed-learner",
    title: "Speed Learner",
    desc: "Finish a lesson in under 5 minutes.",
    xp: 75,
    unlocked: true,
  },
  {
    id: "circuit-builder",
    title: "Circuit Builder",
    desc: "Complete 5 quantum lab sessions.",
    xp: 100,
    unlocked: true,
  },
  {
    id: "precision-solver",
    title: "Precision Solver",
    desc: "Score 90% or more on a problem set.",
    xp: 150,
    unlocked: false,
  },
  {
    id: "teleportation-explorer",
    title: "Teleportation Explorer",
    desc: "Successfully explain teleportation in your own words.",
    xp: 180,
    unlocked: false,
  },
];

export default function AchievementsPage() {
  const unlocked = achievements.filter((achievement) => achievement.unlocked).length;

  return (
    <AppShell>
      <PageHeader
        title="Achievements"
        subtitle="Track milestones across your QuantumVerse learning journey."
        icon={
          <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-yellow-500/30 bg-yellow-500/10">
            <Trophy className="h-5 w-5 text-yellow-400" />
          </div>
        }
      />

      <div className="mb-6 rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-5">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-yellow-300/80">Progress</p>
            <h2 className="mt-2 text-2xl font-bold text-white">
              {unlocked} / {achievements.length} unlocked
            </h2>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-yellow-500/30 bg-yellow-500/10 px-3 py-1.5 text-xs text-yellow-200">
            <Sparkles className="h-4 w-4" />
            Keep learning to unlock more badges
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {achievements.map((achievement) => (
          <div
            key={achievement.id}
            className="rounded-2xl border border-white/10 bg-white/5 p-5"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-center gap-3">
                <div
                  className={`flex h-11 w-11 items-center justify-center rounded-xl ${
                    achievement.unlocked
                      ? "bg-gradient-to-br from-yellow-400 to-orange-500"
                      : "bg-white/5"
                  }`}
                >
                  {achievement.unlocked ? (
                    <CheckCircle2 className="h-5 w-5 text-white" />
                  ) : (
                    <Sparkles className="h-5 w-5 text-muted-foreground" />
                  )}
                </div>
                <div>
                  <h3 className="text-base font-semibold text-white">{achievement.title}</h3>
                  <p className="mt-1 text-sm text-muted-foreground">{achievement.desc}</p>
                </div>
              </div>
              <span className="text-[10px] uppercase tracking-[0.12em] text-quantum-cyan">
                {achievement.xp} XP
              </span>
            </div>
          </div>
        ))}
      </div>
    </AppShell>
  );
}
