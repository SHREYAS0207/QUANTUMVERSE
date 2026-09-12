"use client";

import { cn } from "@/lib/utils";

interface XPProgressProps {
  current: number;
  target: number;
  label?: string;
  showValues?: boolean;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function XPProgress({
  current,
  target,
  label = "XP PROGRESS",
  showValues = true,
  size = "md",
  className,
}: XPProgressProps) {
  const safeTarget = Math.max(target, 1);
  const percentage = Math.min(
    100,
    Math.max(0, (current / safeTarget) * 100)
  );

  const heights = {
    sm: "h-1",
    md: "h-1.5",
    lg: "h-2",
  };

  return (
    <div className={cn("w-full", className)}>
      {(label || showValues) && (
        <div className="mb-2 flex items-center justify-between gap-3">
          {label ? (
            <span className="qv-label text-cyan-300/70">
              {label}
            </span>
          ) : (
            <span />
          )}

          {showValues && (
            <span className="text-xs font-medium tabular-nums text-white/55">
              <span className="text-white">{current.toLocaleString()}</span>
              <span className="mx-1 text-white/20">/</span>
              {target.toLocaleString()} XP
            </span>
          )}
        </div>
      )}

      <div
        className={cn(
          "relative overflow-hidden rounded-full border border-white/[0.07]",
          "bg-white/[0.045]",
          heights[size]
        )}
      >
        <div
          className="absolute inset-y-0 left-0 rounded-full bg-cyan-400 transition-[width] duration-700 ease-out"
          style={{ width: `${percentage}%` }}
        />

        <div
          aria-hidden="true"
          className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-cyan-300 via-cyan-400 to-violet-400 opacity-70 blur-[3px]"
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="mt-1.5 text-right text-[10px] font-medium tracking-wide text-white/30">
        {Math.round(percentage)}%
      </div>
    </div>
  );
}