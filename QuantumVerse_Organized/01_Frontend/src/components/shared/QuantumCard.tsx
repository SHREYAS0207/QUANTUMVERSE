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

export function QuantumCard({ children, className, hover = false, glow = false, onClick }: QuantumCardProps) {
  return (
    <motion.div
      whileHover={hover ? { scale: 1.01, y: -2 } : undefined}
      onClick={onClick}
      className={cn(
        "glass rounded-xl p-5 transition-all duration-300",
        hover && "cursor-pointer glass-hover",
        glow && "border-quantum-blue/30 shadow-[0_0_20px_rgba(0,212,255,0.1)]",
        className
      )}
    >
      {children}
    </motion.div>
  );
}
