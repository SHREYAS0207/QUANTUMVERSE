"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Users, Zap, BookOpen, Trophy, TrendingUp, Activity,
  Database, Server, RefreshCw,
} from "lucide-react";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { PageHeader } from "@/components/shared/PageHeader";
import { StatCard } from "@/components/shared/StatCard";

// ── Mock analytics data ──────────────────────────────────────────────
const DAILY_USERS = [
  { date: "Mon", users: 42 }, { date: "Tue", users: 58 },
  { date: "Wed", users: 71 }, { date: "Thu", users: 65 },
  { date: "Fri", users: 89 }, { date: "Sat", users: 54 },
  { date: "Sun", users: 38 },
];

const LEVEL_DIST = [
  { name: "1-5",   value: 45, color: "#00d4ff" },
  { name: "6-10",  value: 28, color: "#a855f7" },
  { name: "11-20", value: 18, color: "#22c55e" },
  { name: "21+",   value:  9, color: "#f59e0b" },
];

const ALGO_RUNS = [
  { name: "Grover",       runs: 1240 },
  { name: "Teleportation",runs:  980 },
  { name: "DJ",           runs:  760 },
  { name: "QFT",          runs:  540 },
];

const CIRCUIT_SAVES = [
  { week: "W1", saves: 120 }, { week: "W2", saves: 184 },
  { week: "W3", saves: 210 }, { week: "W4", saves: 267 },
  { week: "W5", saves: 312 }, { week: "W6", saves: 298 },
];

const TOOLTIP_STYLE = {
  contentStyle: { background: "#0d0d1a", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 12, fontSize: 12 },
  labelStyle:   { color: "#a0a0b0" },
  itemStyle:    { color: "#00d4ff" },
};

export default function AdminPage() {
  const [refreshing, setRefreshing] = useState(false);

  function handleRefresh() {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 1200);
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
      <div className="flex items-center justify-between">
        <PageHeader
          icon={<Server className="w-6 h-6 text-quantum-blue" />}
          title="Admin Dashboard"
          subtitle="Platform analytics and system health"
        />
        <button onClick={handleRefresh}
          className="flex items-center gap-2 text-sm text-muted-foreground hover:text-white transition-colors">
          <RefreshCw className={`w-4 h-4 ${refreshing ? "animate-spin text-quantum-blue" : ""}`} />
          Refresh
        </button>
      </div>

      {/* KPI row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { icon: Users,    label: "Total Users",      value: "2,847",  delta: "+14%",  up: true  },
          { icon: Zap,      label: "Total XP Awarded", value: "1.2M",   delta: "+23%",  up: true  },
          { icon: BookOpen, label: "Lessons Completed",value: "18,420", delta: "+8%",   up: true  },
          { icon: Trophy,   label: "Quiz Attempts",    value: "9,104",  delta: "-3%",   up: false },
        ].map((stat, i) => (
          <motion.div key={stat.label} initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
            transition={{ delay: i * 0.08 }}
            className="glass rounded-xl border border-white/5 p-5">
            <div className="flex items-center justify-between mb-3">
              <stat.icon className="w-5 h-5 text-quantum-blue" />
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                stat.up ? "text-green-400 bg-green-400/10" : "text-red-400 bg-red-400/10"
              }`}>{stat.delta}</span>
            </div>
            <p className="text-2xl font-bold text-white">{stat.value}</p>
            <p className="text-xs text-muted-foreground mt-1">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      {/* Charts row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* DAU */}
        <div className="lg:col-span-2 glass rounded-xl border border-white/5 p-6">
          <h3 className="text-sm font-semibold text-white mb-5">Daily Active Users (7d)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={DAILY_USERS}>
              <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <Tooltip {...TOOLTIP_STYLE} />
              <Bar dataKey="users" fill="#00d4ff" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Level distribution */}
        <div className="glass rounded-xl border border-white/5 p-6">
          <h3 className="text-sm font-semibold text-white mb-5">User Level Distribution</h3>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie data={LEVEL_DIST} cx="50%" cy="50%" innerRadius={45} outerRadius={70}
                paddingAngle={4} dataKey="value">
                {LEVEL_DIST.map((entry, i) => <Cell key={i} fill={entry.color} />)}
              </Pie>
              <Tooltip {...TOOLTIP_STYLE} formatter={(v: any) => [`${v}%`, "Users"]} />
            </PieChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-2 gap-2 mt-3">
            {LEVEL_DIST.map(d => (
              <div key={d.name} className="flex items-center gap-1.5">
                <div className="w-2 h-2 rounded-full" style={{ background: d.color }} />
                <span className="text-xs text-muted-foreground">Lvl {d.name}</span>
                <span className="text-xs text-white ml-auto">{d.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Charts row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Algorithm popularity */}
        <div className="glass rounded-xl border border-white/5 p-6">
          <h3 className="text-sm font-semibold text-white mb-5">Algorithm Runs (All Time)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={ALGO_RUNS} layout="vertical">
              <XAxis type="number" tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <YAxis dataKey="name" type="category" tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} width={90} />
              <Tooltip {...TOOLTIP_STYLE} />
              <Bar dataKey="runs" fill="#a855f7" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Circuit saves trend */}
        <div className="glass rounded-xl border border-white/5 p-6">
          <h3 className="text-sm font-semibold text-white mb-5">Circuit Saves (6 Weeks)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={CIRCUIT_SAVES}>
              <XAxis dataKey="week" tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 11, fill: "#6b6b80" }} axisLine={false} tickLine={false} />
              <Tooltip {...TOOLTIP_STYLE} />
              <Line type="monotone" dataKey="saves" stroke="#22c55e" strokeWidth={2}
                dot={{ fill: "#22c55e", r: 4 }} activeDot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* System health */}
      <div className="glass rounded-xl border border-white/5 p-6">
        <h3 className="text-sm font-semibold text-white mb-5 flex items-center gap-2">
          <Activity className="w-4 h-4 text-quantum-blue" />
          System Health
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "API Latency",      value: "48ms",    status: "ok"   },
            { label: "DB Connections",   value: "12 / 100", status: "ok"  },
            { label: "Qiskit Jobs/min",  value: "340",     status: "ok"   },
            { label: "Error Rate",       value: "0.12%",   status: "warn" },
          ].map(item => (
            <div key={item.label} className="p-4 rounded-xl bg-white/3 border border-white/5">
              <div className="flex items-center gap-2 mb-2">
                <div className={`w-2 h-2 rounded-full ${
                  item.status === "ok" ? "bg-green-400" : "bg-yellow-400"
                }`} />
                <p className="text-xs text-muted-foreground">{item.label}</p>
              </div>
              <p className="text-lg font-bold text-white">{item.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
