"use client";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface GlowButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  loading?: boolean;
  children: React.ReactNode;
}

export function GlowButton({ variant = "primary", loading, children, className, ...props }: GlowButtonProps) {
  const base = "flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm transition-all disabled:opacity-60";
  const variants = {
    primary:   "bg-quantum-blue text-quantum-dark hover:opacity-90 shadow-[0_0_20px_rgba(0,212,255,0.3)] hover:shadow-[0_0_30px_rgba(0,212,255,0.5)]",
    secondary: "border border-quantum-blue/30 text-quantum-blue hover:bg-quantum-blue/10",
    danger:    "bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20",
    ghost:     "text-muted-foreground hover:text-white hover:bg-white/5",
  };

  return (
    <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
      className={cn(base, variants[variant], className)} disabled={loading} {...(props as any)}>
      {loading && <div className="w-4 h-4 border-2 border-current/30 border-t-current rounded-full animate-spin" />}
      {children}
    </motion.button>
  );
}
