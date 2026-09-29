"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { useAuthStore } from "@/stores/authStore";
import { cn, getXPProgress } from "@/lib/utils";
import {
  LayoutDashboard, BookOpen, FlaskConical, Zap, Bot, Trophy, TrendingUp, User, Settings, LogOut, Atom
} from "lucide-react";

const ICON_MAP: Record<string, React.ElementType> = {
  LayoutDashboard, BookOpen, FlaskConical, Zap, Bot, Trophy, TrendingUp, User, Settings, Atom,
};

const NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard", icon: "LayoutDashboard" },
  { href: "/learn", label: "Learn", icon: "BookOpen" },
  { href: "/quantum-lab", label: "Quantum Lab", icon: "FlaskConical" },
  { href: "/quantum-models", label: "Quantum Models", icon: "Atom" },
  { href: "/algorithms", label: "Algorithms", icon: "Zap" },
  { href: "/ai-tutor", label: "AI Tutor", icon: "Bot" },
  { href: "/quiz", label: "Quiz Arena", icon: "Trophy" },
  { href: "/progress", label: "Progress", icon: "TrendingUp" },
  { href: "/profile", label: "Profile", icon: "User" },
  { href: "/settings", label: "Settings", icon: "Settings" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, clearAuth } = useAuthStore();
  const xpProgress = getXPProgress(user?.xp ?? 0);

  return (
    <aside className="fixed left-0 top-0 z-50 flex h-full w-64 flex-col border-r border-white/[0.07] bg-[#04070a]/88 backdrop-blur-2xl">
      <div className="absolute right-0 top-0 h-full w-px bg-gradient-to-b from-cyan-300/25 via-cyan-300/5 to-purple-400/15" />

      <div className="relative border-b border-white/[0.07] p-5">
        <Link href="/dashboard" className="group flex items-center gap-3">
          <div className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-300/25 bg-cyan-300/[0.06] shadow-[0_0_24px_rgba(0,225,255,.08)]">
            <div className="absolute inset-1 rounded-lg border border-white/[0.04]" />
            <Atom className="h-5 w-5 text-cyan-200 transition-transform duration-500 group-hover:rotate-180" />
          </div>
          <div>
            <p className="text-[13px] font-semibold tracking-[0.19em] text-white">QUANTUM<span className="text-cyan-300">VERSE</span></p>
            <p className="mt-0.5 font-mono text-[9px] uppercase tracking-[0.24em] text-white/35">Quantum Research OS</p>
          </div>
        </Link>
      </div>

      {user && (
        <div className="relative border-b border-white/[0.06] px-4 py-4">
          <div className="mb-2 flex items-center justify-between">
            <span className="qv-label">Explorer Level {user.level}</span>
            <span className="font-mono text-[10px] text-cyan-300">{user.xp} XP</span>
          </div>
          <div className="h-1 overflow-hidden rounded-full bg-white/[0.055]">
            <motion.div
              className="h-full rounded-full bg-gradient-to-r from-cyan-300 via-teal-300 to-violet-400 shadow-[0_0_14px_rgba(0,230,255,.42)]"
              initial={{ width: 0 }}
              animate={{ width: `${xpProgress}%` }}
              transition={{ duration: 1.1, ease: "easeOut" }}
            />
          </div>
        </div>
      )}

      <nav className="flex-1 overflow-y-auto p-3">
        <div className="mb-2 px-3 pt-1 font-mono text-[9px] uppercase tracking-[0.25em] text-white/20">Research Console</div>
        <div className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = ICON_MAP[item.icon];
            const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <Link key={item.href} href={item.href} className="block">
                <motion.div
                  whileHover={{ x: 3 }}
                  transition={{ duration: .18 }}
                  className={cn(
                    "group relative flex items-center gap-3 rounded-xl border px-3 py-2.5 text-[13px] transition-all duration-200",
                    isActive
                      ? "border-cyan-300/20 bg-cyan-300/[0.075] text-cyan-200 shadow-[inset_0_0_22px_rgba(0,220,255,.035),0_0_22px_rgba(0,220,255,.04)]"
                      : "border-transparent text-white/48 hover:border-white/[0.06] hover:bg-white/[0.035] hover:text-white/90"
                  )}
                >
                  {isActive && <span className="absolute left-0 top-2 bottom-2 w-px bg-cyan-300 shadow-[0_0_10px_rgba(0,235,255,.8)]" />}
                  <Icon className={cn("h-4 w-4 shrink-0", isActive ? "text-cyan-200" : "text-white/38 group-hover:text-cyan-200")} />
                  <span>{item.label}</span>
                  {isActive && (
                    <motion.span layoutId="qv-active-nav" className="ml-auto h-1.5 w-1.5 rounded-full bg-cyan-200 shadow-[0_0_10px_rgba(0,235,255,.9)]" />
                  )}
                </motion.div>
              </Link>
            );
          })}
        </div>
      </nav>

      <div className="border-t border-white/[0.07] p-4">
        <div className="mb-3 flex items-center gap-3 rounded-xl border border-white/[0.06] bg-white/[0.018] p-2.5">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-cyan-300/20 bg-cyan-300/[0.07] text-xs font-bold text-cyan-200">
            {user?.name?.[0]?.toUpperCase() ?? "Q"}
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-medium text-white/90">{user?.name ?? "Quantum Explorer"}</p>
            <p className="truncate text-[10px] capitalize text-white/35">{user?.learning_level ?? "beginner"} · active researcher</p>
          </div>
        </div>
        <button
          onClick={clearAuth}
          className="qv-focus flex w-full items-center gap-2 rounded-lg px-3 py-2 text-xs text-white/35 transition-all hover:bg-red-400/[0.05] hover:text-red-300"
        >
          <LogOut className="h-3.5 w-3.5" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
