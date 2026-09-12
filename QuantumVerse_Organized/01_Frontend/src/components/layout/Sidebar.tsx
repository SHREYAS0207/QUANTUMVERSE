"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { useAuthStore } from "@/stores/authStore";
import { cn, getXPProgress } from "@/lib/utils";
import {
  LayoutDashboard, BookOpen, FlaskConical, Zap, Bot, Trophy, Star, TrendingUp, User, Settings, LogOut, Atom
} from "lucide-react";

const ICON_MAP: Record<string, React.ElementType> = {
  LayoutDashboard, BookOpen, FlaskConical, Zap, Bot, Trophy, Star, TrendingUp, User, Settings,
};

const NAV_ITEMS = [
  { href: "/dashboard",    label: "Dashboard",    icon: "LayoutDashboard" },
  { href: "/learn",        label: "Learn",         icon: "BookOpen" },
  { href: "/quantum-lab",  label: "Quantum Lab",   icon: "FlaskConical" },
  { href: "/algorithms",   label: "Algorithms",    icon: "Zap" },
  { href: "/ai-tutor",     label: "AI Tutor",      icon: "Bot" },
  { href: "/quiz",         label: "Quiz Arena",    icon: "Trophy" },
  { href: "/progress",     label: "Progress",      icon: "TrendingUp" },
  { href: "/profile",      label: "Profile",       icon: "User" },
  { href: "/settings",     label: "Settings",      icon: "Settings" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, clearAuth } = useAuthStore();
  const xpProgress = getXPProgress(user?.xp ?? 0);

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-[rgba(0,0,0,0.84)] border-r border-[#00fff0]/15 flex flex-col z-50 backdrop-blur-xl">
      {/* Logo */}
      <div className="p-6 border-b border-[#00fff0]/10">
        <Link href="/dashboard" className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#00fff0]/20 to-[#bf00ff]/20 border border-[#00fff0]/30 flex items-center justify-center shadow-[0_0_18px_rgba(0,255,240,0.18)]">
            <Atom className="w-5 h-5 text-[#00fff0]" />
          </div>
          <div>
            <p className="font-bold text-sm tracking-[0.18em] uppercase text-transparent bg-gradient-to-r from-[#00fff0] via-[#bf00ff] to-[#ff003c] bg-clip-text">QuantumVerse</p>
            <p className="text-[10px] text-[#00fff0]/70 font-mono tracking-[0.22em] uppercase">AI Platform</p>
          </div>
        </Link>
      </div>

      {/* XP Bar */}
      {user && (
        <div className="px-4 py-3 border-b border-[#00fff0]/10">
          <div className="flex justify-between text-xs mb-1">
            <span className="text-muted-foreground">Level {user.level}</span>
            <span className="text-[#00fff0] font-mono">{user.xp} XP</span>
          </div>
          <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-[#00fff0] via-[#bf00ff] to-[#ff003c] rounded-full shadow-[0_0_12px_rgba(0,255,240,0.5)]"
              initial={{ width: 0 }}
              animate={{ width: `${xpProgress}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
            />
          </div>
        </div>
      )}

      {/* Nav */}
      <nav className="flex-1 p-3 space-y-0.5 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = ICON_MAP[item.icon];
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link key={item.href} href={item.href}>
              <motion.div
                whileHover={{ x: 4 }}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200",
                  isActive
                    ? "bg-[rgba(0,255,240,0.08)] text-[#00fff0] border border-[#00fff0]/20 shadow-[0_0_18px_rgba(0,255,240,0.10)]"
                    : "text-muted-foreground hover:text-white hover:bg-white/5"
                )}
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
                {isActive && (
                  <motion.div
                    layoutId="activeNav"
                    className="ml-auto w-1.5 h-1.5 rounded-full bg-[#00fff0] shadow-[0_0_10px_rgba(0,255,240,0.8)]"
                  />
                )}
              </motion.div>
            </Link>
          );
        })}
      </nav>

      {/* User footer */}
      <div className="p-4 border-t border-[#00fff0]/10">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center text-xs font-bold text-white">
            {user?.name?.[0]?.toUpperCase() ?? "Q"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">{user?.name ?? "Quantum Explorer"}</p>
            <p className="text-xs text-muted-foreground capitalize">{user?.learning_level ?? "beginner"}</p>
          </div>
        </div>
        <button
          onClick={clearAuth}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-muted-foreground hover:text-red-400 hover:bg-red-400/5 transition-all"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
