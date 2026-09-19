"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Atom, BookOpen, FlaskConical, LayoutDashboard, Brain, Trophy, ChevronDown, Zap } from "lucide-react";
import { useAuthStore } from "@/stores/authStore";

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Learn", href: "/learn", icon: BookOpen },
  { label: "Quantum Lab", href: "/quantum-lab", icon: FlaskConical },
  { label: "AI Tutor", href: "/ai-tutor", icon: Brain },
  { label: "Quizzes", href: "/quiz", icon: Trophy },
];

export default function QlearnNavbar() {
  const pathname = usePathname();
  const { user } = useAuthStore();
  const firstName = user?.name?.split(" ")[0] || "Explorer";
  const initials = user?.name?.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase() || "QV";

  return (
    <header className="sticky top-0 z-40 ml-64 border-b border-white/[0.07] bg-[#05080b]/72 backdrop-blur-2xl">
      <div className="flex h-16 items-center justify-between px-5 sm:px-6">
        <Link href="/dashboard" className="group flex items-center gap-3">
          <div className="relative flex h-8 w-8 items-center justify-center rounded-lg border border-cyan-300/20 bg-cyan-300/[0.05]">
            <Atom className="h-4 w-4 text-cyan-200 transition-transform duration-500 group-hover:rotate-90" />
          </div>
          <div className="hidden sm:block">
            <div className="text-[11px] font-semibold tracking-[0.2em] text-white/90">QUANTUM<span className="text-cyan-300">VERSE</span></div>
            <div className="font-mono text-[8px] uppercase tracking-[0.24em] text-white/25">Precision learning environment</div>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 lg:flex">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`qv-focus relative flex items-center gap-2 rounded-lg border px-3 py-2 text-[11px] font-medium transition-all ${
                  active
                    ? "border-cyan-300/15 bg-cyan-300/[0.06] text-cyan-200"
                    : "border-transparent text-white/40 hover:border-white/[0.05] hover:bg-white/[0.025] hover:text-white/80"
                }`}
              >
                {active && <span className="absolute inset-x-3 -bottom-[13px] h-px bg-gradient-to-r from-transparent via-cyan-300/70 to-transparent" />}
                <Icon className="h-3.5 w-3.5" />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-3">
          <div className="hidden items-center gap-1.5 rounded-full border border-white/[0.06] bg-white/[0.025] px-2.5 py-1.5 sm:flex">
            <Zap className="h-3.5 w-3.5 text-amber-300" />
            <span className="font-mono text-[10px] text-white/75">{user?.xp ?? 0}</span>
            <span className="text-[9px] uppercase tracking-wider text-white/25">XP</span>
          </div>

          <div className="hidden h-5 w-px bg-white/[0.08] sm:block" />

          <Link href="/profile" className="qv-focus group flex items-center gap-2 rounded-lg px-1.5 py-1 transition-colors hover:bg-white/[0.035]">
            <div className="relative flex h-8 w-8 items-center justify-center rounded-full border border-cyan-300/20 bg-cyan-300/[0.06] text-[10px] font-bold text-cyan-200">
              {initials}
              <span className="absolute -bottom-0.5 -right-0.5 h-2 w-2 rounded-full border-2 border-[#05080b] bg-emerald-300" />
            </div>
            <div className="hidden text-left md:block">
              <div className="max-w-[110px] truncate text-[11px] font-semibold text-white/85">{firstName}</div>
              <div className="font-mono text-[8px] uppercase tracking-wider text-white/25">LVL {user?.level ?? 1}{user?.streak_days ? ` · ${user.streak_days}D` : ""}</div>
            </div>
            <ChevronDown className="hidden h-3.5 w-3.5 text-white/25 transition-transform group-hover:translate-y-0.5 md:block" />
          </Link>
        </div>
      </div>
    </header>
  );
}
