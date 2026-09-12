"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface GlowButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  loading?: boolean;
  children: React.ReactNode;
}

export function GlowButton({
  variant = "primary",
  loading = false,
  children,
  className,
  disabled,
  type = "button",
  onClick,
  name,
  value,
  id,
  title,
  "aria-label": ariaLabel,
  "aria-describedby": ariaDescribedBy,
}: GlowButtonProps) {
  const base =
    "relative inline-flex items-center justify-center gap-2 overflow-hidden rounded-xl px-5 py-2.5 text-sm font-semibold " +
    "transition-[background-color,border-color,color,box-shadow,transform] duration-200 " +
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400/60 " +
    "focus-visible:ring-offset-2 focus-visible:ring-offset-black " +
    "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50";

  const variants = {
    primary:
      "border border-cyan-300/20 bg-cyan-400 text-black " +
      "shadow-[0_0_24px_rgba(0,212,255,0.18)] " +
      "hover:bg-cyan-300 hover:shadow-[0_0_34px_rgba(0,212,255,0.28)]",

    secondary:
      "border border-cyan-400/20 bg-cyan-400/[0.06] text-cyan-200 " +
      "hover:border-cyan-400/35 hover:bg-cyan-400/[0.11] hover:text-cyan-100 " +
      "hover:shadow-[0_0_24px_rgba(0,212,255,0.08)]",

    danger:
      "border border-red-400/20 bg-red-500/[0.08] text-red-300 " +
      "hover:border-red-400/35 hover:bg-red-500/[0.14] hover:text-red-200 " +
      "hover:shadow-[0_0_24px_rgba(239,68,68,0.10)]",

    ghost:
      "border border-transparent bg-transparent text-white/55 " +
      "hover:border-white/[0.08] hover:bg-white/[0.05] hover:text-white",
  };

  return (
    <motion.button
      type={type}
      id={id}
      name={name}
      value={value}
      title={title}
      aria-label={ariaLabel}
      aria-describedby={ariaDescribedBy}
      onClick={onClick}
      disabled={disabled || loading}
      whileHover={disabled || loading ? undefined : { y: -1 }}
      whileTap={disabled || loading ? undefined : { scale: 0.98 }}
      transition={{ duration: 0.15 }}
      className={cn(base, variants[variant], className)}
    >
      {variant === "primary" && (
        <span
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 bg-gradient-to-r from-transparent via-white/[0.12] to-transparent opacity-0 transition-opacity duration-300"
        />
      )}

      {loading && (
        <span
          aria-hidden="true"
          className="h-4 w-4 animate-spin rounded-full border-2 border-current/25 border-t-current"
        />
      )}

      <span className="relative z-10">{children}</span>
    </motion.button>
  );
}