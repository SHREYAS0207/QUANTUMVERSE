"use client";

import { cn } from "@/lib/utils";

interface QuantumBadgeProps {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "danger" | "purple" | "muted";
  className?: string;
  dot?: boolean;
}

export function QuantumBadge({
  children,
  variant = "default",
  className,
  dot = false,
}: QuantumBadgeProps) {
  const variants = {
    default:
      "border-cyan-400/20 bg-cyan-400/[0.08] text-cyan-300",
    success:
      "border-emerald-400/20 bg-emerald-400/[0.08] text-emerald-300",
    warning:
      "border-amber-400/20 bg-amber-400/[0.08] text-amber-300",
    danger:
      "border-red-400/20 bg-red-400/[0.08] text-red-300",
    purple:
      "border-violet-400/20 bg-violet-400/[0.08] text-violet-300",
    muted:
      "border-white/[0.08] bg-white/[0.04] text-white/55",
  };

  const dots = {
    default: "bg-cyan-400",
    success: "bg-emerald-400",
    warning: "bg-amber-400",
    danger: "bg-red-400",
    purple: "bg-violet-400",
    muted: "bg-white/40",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1",
        "text-[11px] font-semibold uppercase tracking-[0.08em]",
        "backdrop-blur-sm transition-colors duration-200",
        variants[variant],
        className
      )}
    >
      {dot && (
        <span
          aria-hidden="true"
          className={cn(
            "h-1.5 w-1.5 rounded-full shadow-[0_0_8px_currentColor]",
            dots[variant]
          )}
        />
      )}

      {children}
    </span>
  );
}