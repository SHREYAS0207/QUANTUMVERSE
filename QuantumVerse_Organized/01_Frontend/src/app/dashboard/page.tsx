"use client";

import { motion } from "framer-motion";
import {
  Zap,
  BookOpen,
  FlaskConical,
  Trophy,
  Flame,
  TrendingUp,
  ArrowRight,
  Play,
} from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/shared/PageHeader";
import { QuantumCard } from "@/components/shared/QuantumCard";
import { StatCard } from "@/components/shared/StatCard";
import { XPProgress } from "@/components/shared/XPProgress";
import { QuantumBadge } from "@/components/shared/QuantumBadge";
import { useAuthStore } from "@/stores/authStore";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import Link from "next/link";
import { cn } from "@/lib/utils";

const MOCK_ACTIVITY = [
  { day: "Mon", minutes: 30 },
  { day: "Tue", minutes: 45 },
  { day: "Wed", minutes: 20 },
  { day: "Thu", minutes: 60 },
  { day: "Fri", minutes: 35 },
  { day: "Sat", minutes: 50 },
  { day: "Sun", minutes: 0 },
];

export default function DashboardPage() {
  const { user } = useAuthStore();

  const stats = [
    {
      label: "Total XP",
      value: user?.xp ?? 0,
      description: "Experience earned",
      icon: <Zap className="h-5 w-5" />,
      className: "hover:border-cyan-400/20",
    },
    {
      label: "Lessons Done",
      value: user?.statistics?.total_lessons ?? 0,
      description: "Lessons completed",
      icon: <BookOpen className="h-5 w-5" />,
      className: "hover:border-blue-400/20",
    },
    {
      label: "Circuits Built",
      value: user?.statistics?.total_circuits ?? 0,
      description: "Quantum experiments",
      icon: <FlaskConical className="h-5 w-5" />,
      className: "hover:border-violet-400/20",
    },
    {
      label: "Quiz Accuracy",
      value: `${user?.statistics?.quiz_accuracy ?? 0}%`,
      description: "Average performance",
      icon: <Trophy className="h-5 w-5" />,
      className: "hover:border-emerald-400/20",
    },
  ];

  const currentXP = user?.xp ?? 0;

  /*
   * Keep the existing user XP data while providing a sensible
   * visual level target. This is presentation-only.
   */
  const level = user?.level ?? 1;
  const nextLevelXP = Math.max(level * 1000, 1000);

  return (
    <AppShell>
      <PageHeader
        eyebrow="QLEARN // DASHBOARD"
        title={`Welcome back, ${user?.name?.split(" ")[0] ?? "Explorer"}`}
        subtitle="Continue your quantum computing journey."
        icon={<Zap className="h-5 w-5" />}
        action={
          <Link href="/quantum-lab">
            <span className="inline-flex items-center gap-2 rounded-xl border border-cyan-300/20 bg-cyan-400 px-4 py-2.5 text-sm font-semibold text-black shadow-[0_0_24px_rgba(0,212,255,0.18)] transition-all hover:bg-cyan-300 hover:shadow-[0_0_34px_rgba(0,212,255,0.28)]">
              Open Lab
              <ArrowRight className="h-4 w-4" />
            </span>
          </Link>
        }
      />

      {/* Learning status */}
      <div className="mb-6 grid grid-cols-1 gap-4 lg:grid-cols-[1fr_auto]">
        <QuantumCard className="relative overflow-hidden p-5 sm:p-6">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -right-16 -top-16 h-40 w-40 rounded-full bg-cyan-400/[0.08] blur-3xl"
          />

          <div className="relative">
            <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="qv-label text-cyan-400/70">CURRENT LEVEL</p>
                <div className="mt-1 flex items-center gap-3">
                  <h2 className="text-2xl font-semibold text-white">
                    Level {level}
                  </h2>

                  <QuantumBadge variant="default" dot>
                    Quantum Explorer
                  </QuantumBadge>
                </div>
              </div>

              <div className="hidden text-right sm:block">
                <p className="text-xs text-white/35">TOTAL XP</p>
                <p className="mt-1 text-lg font-semibold tabular-nums text-cyan-300">
                  {currentXP.toLocaleString()}
                </p>
              </div>
            </div>

            <XPProgress
              current={currentXP % nextLevelXP}
              target={nextLevelXP}
              label={`LEVEL ${level + 1} PROGRESS`}
            />
          </div>
        </QuantumCard>

        {(user?.streak_days ?? 0) > 0 && (
          <motion.div
            initial={{ opacity: 0, x: 15 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex min-w-[210px] items-center gap-4 rounded-2xl border border-orange-400/15 bg-orange-400/[0.05] px-5 py-4 backdrop-blur-xl"
          >
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-orange-400/20 bg-orange-400/[0.08]">
              <Flame className="h-5 w-5 text-orange-300" />
            </div>

            <div>
              <p className="qv-label text-orange-300/60">ACTIVE STREAK</p>
              <p className="mt-1 text-lg font-semibold text-white">
                {user?.streak_days} days
              </p>
              <p className="text-xs text-white/35">Keep the momentum going.</p>
            </div>
          </motion.div>
        )}
      </div>

      {/* Stats */}
      <div className="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.06, duration: 0.25 }}
          >
            <StatCard {...stat} />
          </motion.div>
        ))}
      </div>

      {/* Main dashboard content */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,1.7fr)_minmax(300px,0.8fr)]">
        {/* Activity */}
        <QuantumCard className="p-5 sm:p-6">
          <div className="mb-6 flex items-start justify-between gap-4">
            <div>
              <p className="qv-label text-cyan-400/60">LEARNING ACTIVITY</p>
              <h2 className="mt-1 text-lg font-semibold text-white">
                Weekly Activity
              </h2>
              <p className="mt-1 text-xs text-white/35">
                Minutes spent learning this week
              </p>
            </div>

            <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-cyan-400/15 bg-cyan-400/[0.06]">
              <TrendingUp className="h-4 w-4 text-cyan-300" />
            </div>
          </div>

          <ResponsiveContainer width="100%" height={190}>
            <BarChart
              data={MOCK_ACTIVITY}
              margin={{ top: 8, right: 5, left: -28, bottom: 0 }}
            >
              <XAxis
                dataKey="day"
                tick={{
                  fill: "#64748b",
                  fontSize: 11,
                }}
                axisLine={false}
                tickLine={false}
              />

              <YAxis hide />

              <Tooltip
                cursor={{ fill: "rgba(255,255,255,0.025)" }}
                contentStyle={{
                  background: "#080b10",
                  border: "1px solid rgba(0,212,255,0.16)",
                  borderRadius: "12px",
                  color: "#e2e8f0",
                  boxShadow: "0 12px 30px rgba(0,0,0,0.35)",
                }}
                labelStyle={{
                  color: "#94a3b8",
                  marginBottom: "4px",
                }}
                formatter={(value) => [`${value} min`, "Learning"]}
              />

              <Bar
                dataKey="minutes"
                fill="rgba(0,212,255,0.75)"
                radius={[6, 6, 2, 2]}
                maxBarSize={34}
              />
            </BarChart>
          </ResponsiveContainer>
        </QuantumCard>

        {/* Quick Actions */}
        <QuantumCard className="p-5 sm:p-6">
          <div className="mb-5">
            <p className="qv-label text-cyan-400/60">SHORTCUTS</p>
            <h2 className="mt-1 text-lg font-semibold text-white">
              Quick Actions
            </h2>
            <p className="mt-1 text-xs text-white/35">
              Jump directly into your next activity.
            </p>
          </div>

          <div className="space-y-2">
            {[
              {
                href: "/learn",
                label: "Continue Learning",
                icon: BookOpen,
                color: "text-blue-300",
                bg: "bg-blue-400/[0.07]",
              },
              {
                href: "/quantum-lab",
                label: "Build a Circuit",
                icon: FlaskConical,
                color: "text-violet-300",
                bg: "bg-violet-400/[0.07]",
              },
              {
                href: "/ai-tutor",
                label: "Ask QubitAI",
                icon: Zap,
                color: "text-cyan-300",
                bg: "bg-cyan-400/[0.07]",
              },
              {
                href: "/quiz",
                label: "Take a Quiz",
                icon: Trophy,
                color: "text-emerald-300",
                bg: "bg-emerald-400/[0.07]",
              },
            ].map((action) => (
              <Link key={action.href} href={action.href} className="block">
                <div className="group flex items-center gap-3 rounded-xl border border-transparent px-3 py-3 transition-all duration-200 hover:border-white/[0.07] hover:bg-white/[0.04]">
                  <div
                    className={cn(
                      "flex h-9 w-9 shrink-0 items-center justify-center rounded-lg",
                      action.bg
                    )}
                  >
                    <action.icon className={cn("h-4 w-4", action.color)} />
                  </div>

                  <span className="text-sm font-medium text-white/65 transition-colors group-hover:text-white">
                    {action.label}
                  </span>

                  <ArrowRight className="ml-auto h-3.5 w-3.5 text-white/20 transition-all group-hover:translate-x-0.5 group-hover:text-cyan-300" />
                </div>
              </Link>
            ))}
          </div>

          <Link
            href="/learn"
            className="mt-5 flex items-center justify-center gap-2 rounded-xl border border-white/[0.07] bg-white/[0.025] py-2.5 text-xs font-medium text-white/45 transition-all hover:border-cyan-400/15 hover:bg-cyan-400/[0.05] hover:text-cyan-300"
          >
            <Play className="h-3 w-3" />
            Explore all learning content
          </Link>
        </QuantumCard>
      </div>
    </AppShell>
  );
}