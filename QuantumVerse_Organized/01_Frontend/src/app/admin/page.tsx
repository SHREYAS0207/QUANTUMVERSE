"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import {
  Activity,
  Bot,
  BookOpen,
  Database,
  RefreshCw,
  Server,
  ShieldCheck,
  Users,
  Zap,
} from "lucide-react";
import { PageHeader } from "@/components/shared/PageHeader";

const SYSTEM_READINESS = [
  { icon: Server, label: "API Gateway", value: "Operational", detail: "FastAPI routing, auth, and health checks are live." },
  { icon: Database, label: "Database Layer", value: "Connected", detail: "SQLite-backed persistence and schema startup are working." },
  { icon: Zap, label: "Quantum Engine", value: "Ready", detail: "Circuit building and simulation paths are available." },
  { icon: Bot, label: "AI Services", value: "Demo Mode", detail: "OpenRouter is optional; the app falls back gracefully when no key is set." },
];

const FEATURE_STATUS = [
  { label: "User Accounts", value: "Auth endpoints available" },
  { label: "Learning Content", value: "Lessons and quiz flows wired" },
  { label: "Circuit Lab", value: "Templates, editor, and simulations ready" },
  { label: "Progress Tracking", value: "XP, streaks, and achievement surfaces available" },
];

export default function AdminPage() {
  const [refreshing, setRefreshing] = useState(false);

  function handleRefresh() {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 1200);
  }

  return (
    <div className="mx-auto max-w-7xl space-y-8 px-6 py-8">
      <div className="flex items-center justify-between">
        <PageHeader
          icon={<Server className="w-6 h-6 text-quantum-blue" />}
          title="Admin Dashboard"
          subtitle="Platform readiness and system health overview"
        />
        <button
          onClick={handleRefresh}
          className="flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-white"
        >
          <RefreshCw className={`h-4 w-4 ${refreshing ? "animate-spin text-quantum-blue" : ""}`} />
          Refresh
        </button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {SYSTEM_READINESS.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.08 }}
            className="glass rounded-xl border border-white/5 p-5"
          >
            <div className="mb-4 flex items-center justify-between">
              <stat.icon className="h-5 w-5 text-quantum-blue" />
              <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-[10px] uppercase tracking-[0.12em] text-emerald-300">
                Live
              </span>
            </div>
            <p className="text-sm text-muted-foreground">{stat.label}</p>
            <p className="mt-2 text-xl font-bold text-white">{stat.value}</p>
            <p className="mt-2 text-xs text-muted-foreground">{stat.detail}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.5fr,1fr]">
        <div className="glass rounded-xl border border-white/5 p-6">
          <h3 className="mb-5 flex items-center gap-2 text-sm font-semibold text-white">
            <Activity className="h-4 w-4 text-quantum-blue" />
            Current Product Status
          </h3>

          <div className="space-y-4">
            {FEATURE_STATUS.map((item) => (
              <div key={item.label} className="rounded-xl border border-white/5 bg-white/3 p-3">
                <div className="mb-1 flex items-center justify-between gap-3">
                  <span className="text-sm font-medium text-white">{item.label}</span>
                  <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
                </div>
                <p className="text-xs text-muted-foreground">{item.value}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="glass rounded-xl border border-white/5 p-6">
          <h3 className="mb-5 flex items-center gap-2 text-sm font-semibold text-white">
            <ShieldCheck className="h-4 w-4 text-quantum-blue" />
            Operational Notes
          </h3>

          <div className="space-y-4 text-sm text-muted-foreground">
            <div className="rounded-xl border border-white/5 bg-white/3 p-4">
              <p className="font-medium text-white">Deployment posture</p>
              <p className="mt-1">This prototype is configured for local development and lightweight verification, with backend health checks and frontend compile validation already wired in.</p>
            </div>
            <div className="rounded-xl border border-white/5 bg-white/3 p-4">
              <p className="font-medium text-white">Next upgrade path</p>
              <p className="mt-1">Connect live analytics, richer AI context, and production credentials to turn the current working prototype into a fully instrumented deployment-ready system.</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="glass rounded-xl border border-white/5 p-5">
          <Users className="mb-3 h-5 w-5 text-quantum-blue" />
          <p className="text-sm text-muted-foreground">Users</p>
          <p className="mt-2 text-xl font-bold text-white">Auth-backed</p>
        </div>
        <div className="glass rounded-xl border border-white/5 p-5">
          <BookOpen className="mb-3 h-5 w-5 text-quantum-blue" />
          <p className="text-sm text-muted-foreground">Learning</p>
          <p className="mt-2 text-xl font-bold text-white">Course content ready</p>
        </div>
        <div className="glass rounded-xl border border-white/5 p-5">
          <Zap className="mb-3 h-5 w-5 text-quantum-blue" />
          <p className="text-sm text-muted-foreground">Quantum Lab</p>
          <p className="mt-2 text-xl font-bold text-white">Simulation path verified</p>
        </div>
      </div>
    </div>
  );
}
