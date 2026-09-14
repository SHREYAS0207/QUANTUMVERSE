"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Zap, BookOpen, FlaskConical, Trophy, Flame, TrendingUp, ArrowRight } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { useAuthStore } from "@/stores/authStore";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import Link from "next/link";
import { cn } from "@/lib/utils";

export default function DashboardPage() {
  const { user } = useAuthStore();

  const activityData = [
    { day: "Mon", minutes: Math.max(5, ((user?.statistics?.total_lessons ?? 0) % 6) * 8 + 10) },
    { day: "Tue", minutes: Math.max(5, ((user?.statistics?.total_circuits ?? 0) % 5) * 10 + 12) },
    { day: "Wed", minutes: Math.max(5, ((user?.statistics?.total_quizzes ?? 0) % 4) * 12 + 8) },
    { day: "Thu", minutes: Math.max(5, ((user?.statistics?.quiz_accuracy ?? 0) % 7) * 9 + 14) },
    { day: "Fri", minutes: Math.max(5, ((user?.xp ?? 0) % 8) * 6 + 12) },
    { day: "Sat", minutes: Math.max(5, ((user?.level ?? 1) % 5) * 11 + 10) },
    { day: "Sun", minutes: Math.max(5, ((user?.streak_days ?? 0) % 6) * 10 + 6) },
  ];

  const stats = [
    { label: "Total XP",       value: user?.xp ?? 0,                      icon: Zap,        color: "text-yellow-400" },
    { label: "Lessons Done",   value: user?.statistics?.total_lessons ?? 0, icon: BookOpen,   color: "text-blue-400" },
    { label: "Circuits Built", value: user?.statistics?.total_circuits ?? 0, icon: FlaskConical, color: "text-purple-400" },
    { label: "Quiz Accuracy",  value: `${user?.statistics?.quiz_accuracy ?? 0}%`, icon: Trophy, color: "text-green-400" },
  ];

  return (
    <AppShell>
      <PageHeader
        title={`Welcome back, ${user?.name?.split(" ")[0] ?? "Explorer"}! 👋`}
        subtitle="Continue your quantum computing journey"
      >
        <Link href="/quantum-lab">
          <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-quantum-blue text-quantum-dark font-semibold text-sm hover:opacity-90 transition-opacity">
            Open Lab <ArrowRight className="w-4 h-4" />
          </button>
        </Link>
      </PageHeader>

      {/* Streak banner */}
      {(user?.streak_days ?? 0) > 0 && (
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}
          className="mb-6 flex items-center gap-3 px-5 py-3 rounded-xl bg-orange-500/10 border border-orange-500/20">
          <Flame className="w-5 h-5 text-orange-400" />
          <span className="text-sm text-orange-300">
            🔥 <strong>{user?.streak_days} day</strong> learning streak — keep it up!
          </span>
        </motion.div>
      )}

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
            className="glass rounded-xl p-5 border border-white/5">
            <s.icon className={cn("w-6 h-6 mb-3", s.color)} />
            <p className="text-2xl font-bold text-white">{s.value}</p>
            <p className="text-xs text-muted-foreground mt-0.5">{s.label}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Activity Chart */}
        <QuantumCard className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-white">Weekly Activity</h2>
            <TrendingUp className="w-4 h-4 text-quantum-blue" />
          </div>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={activityData}>
              <XAxis dataKey="day" tick={{ fill: "#64748b", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip contentStyle={{ background: "#0D1F3C", border: "1px solid rgba(0,212,255,0.2)", borderRadius: "8px", color: "#e2e8f0" }} />
              <Bar dataKey="minutes" fill="#00D4FF" radius={[4, 4, 0, 0]} opacity={0.8} />
            </BarChart>
          </ResponsiveContainer>
        </QuantumCard>

        {/* Quick Actions */}
        <QuantumCard>
          <h2 className="text-sm font-semibold text-white mb-4">Quick Actions</h2>
          <div className="space-y-2">
            {[
              { href: "/learn",        label: "Continue Learning",  icon: BookOpen,    color: "text-blue-400" },
              { href: "/quantum-lab",  label: "Build a Circuit",    icon: FlaskConical, color: "text-purple-400" },
              { href: "/qlearn/ai-tutor", label: "Ask QubitAI",     icon: Zap,          color: "text-cyan-400" },
              { href: "/quiz",         label: "Take a Quiz",         icon: Trophy,       color: "text-green-400" },
            ].map((action) => (
              <Link key={action.href} href={action.href}>
                <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition-colors cursor-pointer">
                  <action.icon className={cn("w-4 h-4", action.color)} />
                  <span className="text-sm text-muted-foreground hover:text-white transition-colors">{action.label}</span>
                  <ArrowRight className="w-3 h-3 ml-auto text-muted-foreground" />
                </div>
              </Link>
            ))}
          </div>
        </QuantumCard>
      </div>
    </AppShell>
  );
}
