"use client";

import { motion } from "framer-motion";
import { X } from "lucide-react";
import { GATE_CATALOG } from "@/lib/constants";
import type { GateOperation } from "@/types/circuit";

interface GateBlockProps {
  operation: GateOperation;
  onRemove: (id: string) => void;
}

export function GateBlock({
  operation,
  onRemove,
}: GateBlockProps) {
  const gateInfo = GATE_CATALOG.find(
    (gate) => gate.type === operation.gate
  );

  const color = gateInfo?.color ?? "#64748b";

  const displayLabel =
    operation.gate === "MEASURE"
      ? "M"
      : operation.gate.length <= 3
        ? operation.gate
        : operation.gate.slice(0, 3);

  return (
    <motion.div
      initial={{ scale: 0.65, opacity: 0, y: 4 }}
      animate={{ scale: 1, opacity: 1, y: 0 }}
      exit={{ scale: 0.65, opacity: 0, y: 4 }}
      transition={{
        type: "spring",
        stiffness: 420,
        damping: 24,
      }}
      className="group relative flex h-10 w-10 cursor-pointer items-center justify-center rounded-xl border font-mono text-sm font-bold transition-all duration-200 hover:-translate-y-0.5 hover:scale-110"
      style={{
        borderColor: `${color}70`,
        background: `
          radial-gradient(
            circle at 50% 35%,
            ${color}22 0%,
            ${color}0c 48%,
            transparent 75%
          ),
          rgba(0,0,0,0.35)
        `,
        color,
        boxShadow: `
          0 0 0 1px ${color}08,
          0 0 14px ${color}22,
          inset 0 0 12px ${color}0c
        `,
      }}
      title={gateInfo?.description ?? operation.gate}
    >
      {/* Top highlight */}
      <div
        className="pointer-events-none absolute inset-x-2 top-0 h-px opacity-70"
        style={{
          background: `linear-gradient(90deg, transparent, ${color}, transparent)`,
        }}
      />

      {/* Gate symbol */}
      <span className="relative z-10 drop-shadow-[0_0_6px_currentColor]">
        {displayLabel}
      </span>

      {/* Gate type indicator */}
      {gateInfo?.category && (
        <span
          className="absolute bottom-1 left-1/2 -translate-x-1/2 text-[5px] font-sans uppercase tracking-[0.12em] opacity-40"
          style={{ color }}
        >
          {gateInfo.category === "single"
            ? "1Q"
            : gateInfo.category === "rotation"
              ? "ROT"
              : gateInfo.category === "multi"
                ? "2Q"
                : "MEAS"}
        </span>
      )}

      {/* Hover glow */}
      <div
        className="pointer-events-none absolute -inset-1 -z-10 rounded-xl opacity-0 blur-md transition-opacity duration-200 group-hover:opacity-60"
        style={{
          backgroundColor: color,
        }}
      />

      {/* Remove button */}
      <button
        type="button"
        aria-label={`Remove ${operation.gate} gate`}
        onClick={(event) => {
          event.stopPropagation();
          onRemove(operation.id);
        }}
        className="absolute -right-2 -top-2 z-20 flex h-4 w-4 items-center justify-center rounded-full border border-red-300/20 bg-red-500/90 text-white opacity-0 shadow-lg transition-all duration-150 hover:scale-110 hover:bg-red-400 group-hover:opacity-100"
      >
        <X className="h-2.5 w-2.5" />
      </button>

      {/* Active corner marker */}
      <div
        className="absolute bottom-0.5 right-1 h-0.5 w-1.5 rounded-full opacity-40"
        style={{ backgroundColor: color }}
      />
    </motion.div>
  );
}