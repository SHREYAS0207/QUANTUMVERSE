"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface StatCardProps {
  label: string;
  value: string | number;
  description?: string;
  icon?: React.ReactNode;
  trend?: string;
  trendPositive?: boolean;
  className?: string;
}

export function StatCard({
  label,
  value,
  description,
  icon,
  trend,
  trendPositive = true,
  className,
}: StatCardProps) {
  return (
    <motion.div
      whileHover={{ y: -3 }}
      transition={{ duration: 0.18 }}
      className={cn(
        "group relative overflow-hidden rounded-2xl border border-white/[0.08]",
        "bg-white/[0.025] p-5 backdrop-blur-xl",
        "shadow-[0_12px_40px_rgba(0,0,0,0.18)]",
        "transition-[border-color,background-color,box-shadow] duration-300",
        "hover:border-cyan-400/20 hover:bg-white/[0.04]",
        "hover:shadow-[0_16px_50px_rgba(0,0,0,0.25)]",
        className
      )}
    >
      {/* Ambient glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-10 -top-10 h-28 w-28 rounded-full bg-cyan-400/[0.07] blur-3xl transition-opacity duration-300 group-hover:bg-cyan-400/[0.12]"
      />

      <div className="relative flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="qv-label">{label}</p>

          <p className="mt-3 text-2xl font-semibold tracking-tight text-white sm:text-3xl">
            {value}
          </p>

          {description && (
            <p className="mt-1.5 text-xs leading-5 text-white/40">
              {description}
            </p>
          )}

          {trend && (
            <div
              className={cn(
                "mt-3 inline-flex items-center gap-1 text-xs font-medium",
                trendPositive ? "text-emerald-300" : "text-red-300"
              )}
            >
              <span aria-hidden="true">
                {trendPositive ? "↑" : "↓"}
              </span>
              {trend}
            </div>
          )}
        </div>

        {icon && (
          <div
            className={cn(
              "flex h-10 w-10 shrink-0 items-center justify-center rounded-xl",
              "border border-cyan-400/15 bg-cyan-400/[0.07]",
              "text-cyan-300",
              "transition-all duration-300",
              "group-hover:border-cyan-400/25 group-hover:bg-cyan-400/[0.11]",
              "group-hover:shadow-[0_0_20px_rgba(0,212,255,0.10)]"
            )}
          >
            {icon}
          </div>
        )}
      </div>

      {/* Bottom accent */}
      <div
        aria-hidden="true"
        className="absolute bottom-0 left-5 right-5 h-px bg-gradient-to-r from-transparent via-cyan-400/20 to-transparent opacity-60"
      />
    </motion.div>
  );
}