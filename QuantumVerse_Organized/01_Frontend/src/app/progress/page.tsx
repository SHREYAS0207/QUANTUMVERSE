"use client";
import { useAuthStore } from "@/stores/authStore";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { BookOpen, FlaskConical, Trophy, Zap, Clock, TrendingUp } from "lucide-react";
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from "recharts";

const WEEKLY_DATA = [
  { day: "Mon", minutes: 30 }, { day: "Tue", minutes: 45 }, { day: "Wed", minutes: 20 },
  { day: "Thu", minutes: 60 }, { day: "Fri", minutes: 35 }, { day: "Sat", minutes: 50 }, { day: "Sun", minutes: 10 },
];

export default function ProgressPage() {
  const { user } = useAuthStore();

  const radarData = [
    { topic: "Fundamentals", score: 80 },
    { topic: "Gates",         score: 60 },
    { topic: "Multi-Qubit",  score: 40 },
    { topic: "Algorithms",   score: 20 },
    { topic: "Quiz",          score: user?.statistics?.quiz_accuracy ?? 0 },
  ];

  return (
    <AppShell>
      <PageHeader title="Learning Progress" subtitle="Your quantum mastery journey" />

      {/* Summary stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {[
          { icon: BookOpen,    label: "Lessons Done",  value: user?.statistics?.total_lessons ?? 0, color: "text-blue-400" },
          { icon: FlaskConical,label: "Circuits Built", value: user?.statistics?.total_circuits ?? 0, color: "text-purple-400" },
          { icon: Trophy,      label: "Quizzes",        value: user?.statistics?.total_quizzes ?? 0,  color: "text-yellow-400" },
          { icon: Zap,         label: "Total XP",       value: user?.xp ?? 0,                          color: "text-cyan-400" },
        ].map((s) => (
          <QuantumCard key={s.label}>
            <s.icon className={`w-5 h-5 mb-2 ${s.color}`} />
            <p className="text-xl font-bold text-white">{s.value}</p>
            <p className="text-xs text-muted-foreground">{s.label}</p>
          </QuantumCard>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Weekly chart */}
        <QuantumCard>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-4 h-4 text-quantum-blue" />
            <p className="text-sm font-medium text-white">Weekly Activity (minutes)</p>
          </div>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={WEEKLY_DATA}>
                <XAxis dataKey="day" tick={{ fill: "#64748b", fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis hide />
                <Tooltip contentStyle={{ background: "#0D1F3C", border: "1px solid rgba(0,212,255,0.2)", borderRadius: "8px", color: "#e2e8f0", fontSize: "11px" }} />
                <Bar dataKey="minutes" radius={[4,4,0,0]}>
                  {WEEKLY_DATA.map((_, i) => <Cell key={i} fill={i === 3 ? "#00D4FF" : "#00D4FF55"} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </QuantumCard>

        {/* Skill Radar */}
        <QuantumCard>
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-4 h-4 text-quantum-purple" />
            <p className="text-sm font-medium text-white">Skill Radar</p>
          </div>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.05)" />
                <PolarAngleAxis dataKey="topic" tick={{ fill: "#64748b", fontSize: 10 }} />
                <Radar dataKey="score" fill="rgba(0,212,255,0.2)" stroke="#00D4FF" strokeWidth={2} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </QuantumCard>
      </div>
    </AppShell>
  );
}
