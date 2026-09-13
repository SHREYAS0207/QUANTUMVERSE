"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  Atom, BookOpen, BrainCircuit, Home, Trophy,
  Settings, User, Cpu, HelpCircle, LayoutDashboard,
  FlaskConical, Medal, type LucideIcon,
} from "lucide-react";

const NAV = [
  { label: "Dashboard",   href: "/dashboard",   icon: Home         },
  { label: "Quantum Lab", href: "/quantum-lab",  icon: FlaskConical },
  { label: "Learn",       href: "/learn",        icon: BookOpen     },
  { label: "Algorithms",  href: "/algorithms",   icon: Cpu          },
  { label: "AI Tutor",    href: "/qlearn/ai-tutor", icon: BrainCircuit },
  { label: "Quiz",        href: "/quiz",         icon: HelpCircle   },
] as const;

const SECONDARY = [
  { label: "Progress",      href: "/progress",     icon: LayoutDashboard },
  { label: "Leaderboard",   href: "/leaderboard",  icon: Medal           },
  { label: "Profile",       href: "/profile",      icon: User            },
  { label: "Settings",      href: "/settings",     icon: Settings        },
] as const;

function NavItem({ path, href, icon: Icon, label }: { path: string; href: string; icon: LucideIcon; label: string }) {
  const active = path === href || (href !== "/dashboard" && path.startsWith(href));
  return (
    <Link href={href}
      className={cn(
        "flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all",
        active
          ? "bg-quantum-blue/10 text-quantum-blue border border-quantum-blue/20"
          : "text-muted-foreground hover:text-white hover:bg-white/5",
      )}
    >
      <Icon className="w-4 h-4 flex-shrink-0" />
      {label}
    </Link>
  );
}

export function Sidebar() {
  const path = usePathname();

  return (
    <aside className="w-60 flex-shrink-0 h-screen glass border-r border-white/5 flex flex-col">
      {/* Logo */}
      <div className="p-5 flex items-center gap-2.5 border-b border-white/5">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-quantum-blue to-quantum-purple flex items-center justify-center">
          <Atom className="w-4 h-4 text-quantum-dark" />
        </div>
        <span className="font-bold text-white text-sm">QuantumVerse</span>
      </div>

      {/* Main nav */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {NAV.map(item => <NavItem key={item.href} path={path} {...item} />)}

        <div className="pt-4 pb-2">
          <p className="px-3 text-[10px] font-semibold text-muted-foreground/50 uppercase tracking-wider mb-1">Personal</p>
        </div>
        {SECONDARY.map(item => <NavItem key={item.href} path={path} {...item} />)}
      </nav>

      {/* Admin link */}
      <div className="p-3 border-t border-white/5">
        <NavItem path={path} href="/admin" icon={LayoutDashboard} label="Admin" />
      </div>
    </aside>
  );
}
