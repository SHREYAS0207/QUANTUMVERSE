"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Atom,
  BookOpen,
  FlaskConical,
  LayoutDashboard,
  Brain,
  Trophy,
  ChevronDown,
  Zap,
} from "lucide-react";
import { useAuthStore } from "@/stores/authStore";

const navItems = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "Learn",
    href: "/learn",
    icon: BookOpen,
  },
  {
    label: "Quantum Lab",
    href: "/quantum-lab",
    icon: FlaskConical,
  },
  {
    label: "AI Tutor",
    href: "/ai-tutor",
    icon: Brain,
  },
  {
    label: "Quizzes",
    href: "/quiz",
    icon: Trophy,
  },
];

export default function QlearnNavbar() {
  const pathname = usePathname();
  const { user } = useAuthStore();

  const firstName = user?.name?.split(" ")[0] || "Explorer";
  const initials =
    user?.name
      ?.split(" ")
      .map((part) => part[0])
      .join("")
      .slice(0, 2)
      .toUpperCase() || "QC";

  return (
    <header className="sticky top-0 z-50 ml-64 border-b border-white/10 bg-black/75 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-6">
        {/* Brand */}
        <Link
          href="/dashboard"
          className="flex items-center gap-3 transition-opacity hover:opacity-80"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-cyan-400/30 bg-cyan-400/10">
            <Atom className="h-5 w-5 text-cyan-300" />
          </div>

          <div>
            <div className="text-sm font-bold tracking-wide text-white">
              QUANTUM<span className="text-cyan-300">VERSE</span>
            </div>
            <div className="text-[9px] uppercase tracking-[0.25em] text-white/35">
              Learn · Build · Simulate
            </div>
          </div>
        </Link>

        {/* Navigation */}
        <nav className="hidden items-center gap-1 lg:flex">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active =
              pathname === item.href ||
              pathname.startsWith(`${item.href}/`);

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium transition-all ${
                  active
                    ? "bg-cyan-400/10 text-cyan-300"
                    : "text-white/55 hover:bg-white/5 hover:text-white"
                }`}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* User stats */}
        <div className="flex items-center gap-4">
          <div className="hidden items-center gap-1.5 sm:flex">
            <Zap className="h-4 w-4 text-yellow-300" />
            <span className="text-xs font-semibold text-white">
              {user?.xp ?? 0}
            </span>
            <span className="text-[10px] text-white/35">XP</span>
          </div>

          <div className="hidden h-6 w-px bg-white/10 sm:block" />

          <Link
            href="/profile"
            className="flex items-center gap-2 rounded-lg px-2 py-1.5 transition-colors hover:bg-white/5"
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-full border border-cyan-400/30 bg-cyan-400/10 text-[10px] font-bold text-cyan-300">
              {initials}
            </div>

            <div className="hidden text-left md:block">
              <div className="max-w-[110px] truncate text-xs font-semibold text-white">
                {firstName}
              </div>
              <div className="text-[9px] text-white/35">
                Level {user?.level ?? 1}
                {user?.streak_days
                  ? ` · ${user.streak_days}d streak`
                  : ""}
              </div>
            </div>

            <ChevronDown className="hidden h-3.5 w-3.5 text-white/35 md:block" />
          </Link>
        </div>
      </div>
    </header>
  );
}
