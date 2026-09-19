"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, FlaskConical, BookOpen, BrainCircuit, User } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/dashboard",  icon: Home,          label: "Home"  },
  { href: "/quantum-lab", icon: FlaskConical, label: "Lab"   },
  { href: "/learn",      icon: BookOpen,      label: "Learn" },
  { href: "/ai-tutor",   icon: BrainCircuit,  label: "AI"   },
  { href: "/profile",    icon: User,          label: "Me"   },
];

export function MobileNav() {
  const path = usePathname();
  return (
    <nav className="md:hidden fixed bottom-0 inset-x-0 z-50 glass border-t border-white/5 flex">
      {NAV.map(({ href, icon: Icon, label }) => {
        const active = path === href || (href !== "/dashboard" && path.startsWith(href));
        return (
          <Link key={href} href={href}
            className={cn("flex-1 flex flex-col items-center gap-0.5 py-3 transition-colors",
              active ? "text-quantum-blue" : "text-muted-foreground hover:text-white")}>
            <Icon className="w-5 h-5" />
            <span className="text-[10px] font-medium">{label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
