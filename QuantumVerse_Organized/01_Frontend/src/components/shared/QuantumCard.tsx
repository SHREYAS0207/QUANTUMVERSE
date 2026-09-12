"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface QuantumCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  glow?: boolean;
  onClick?: () => void;
}

export function QuantumCard({
  children,
  className,
  hover = false,
  glow = false,
  onClick,
}: QuantumCardProps) {
  return (
    <motion.div
      whileHover={
        hover
          ? {
              y: -3,
              transition: {
                duration: 0.2,
                ease: "easeOut",
              },
            }
          : undefined
      }
      whileTap={onClick ? { scale: 0.995 } : undefined}
      onClick={onClick}
      className={cn(
        "group relative overflow-hidden rounded-2xl",
        "border border-white/[0.08]",
        "bg-[rgba(8,8,14,0.72)]",
        "backdrop-blur-xl",
        "shadow-[0_12px_40px_rgba(0,0,0,0.18)]",
        "transition-[border-color,box-shadow,background-color] duration-300",

        hover && [
          "cursor-pointer",
          "hover:border-cyan-400/20",
          "hover:bg-[rgba(10,10,17,0.82)]",
          "hover:shadow-[0_16px_50px_rgba(0,0,0,0.28),0_0_30px_rgba(0,212,255,0.06)]",
        ],

        glow && [
          "border-cyan-400/20",
          "shadow-[0_0_30px_rgba(0,212,255,0.08)]",
        ],

        className
      )}
    >
      {/* Subtle top highlight */}
      <div
        className={cn(
          "pointer-events-none absolute inset-x-0 top-0 h-px",
          "bg-gradient-to-r from-transparent via-white/10 to-transparent",
          "opacity-70",
          hover && "group-hover:via-cyan-300/25",
          "transition-opacity duration-300"
        )}
      />

      {/* Hover atmosphere */}
      {hover && (
        <div
          className={cn(
            "pointer-events-none absolute -right-16 -top-16",
            "h-32 w-32 rounded-full",
            "bg-cyan-400/[0.04]",
            "blur-3xl",
            "opacity-0 transition-opacity duration-300",
            "group-hover:opacity-100"
          )}
        />
      )}

      <div className="relative z-10 p-5">
        {children}
      </div>
    </motion.div>
  );
}