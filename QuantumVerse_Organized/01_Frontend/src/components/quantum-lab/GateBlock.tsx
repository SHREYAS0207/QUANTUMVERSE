"use client";
import { motion } from "framer-motion";
import { X } from "lucide-react";
import { GATE_CATALOG } from "@/lib/constants";
import type { GateOperation } from "@/types/circuit";

interface GateBlockProps {
  operation: GateOperation;
  onRemove: (id: string) => void;
}

export function GateBlock({ operation, onRemove }: GateBlockProps) {
  const gateInfo = GATE_CATALOG.find((g) => g.type === operation.gate);
  const color = gateInfo?.color ?? "#64748b";

  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0, opacity: 0 }}
      className="relative group w-10 h-10 rounded-lg border flex items-center justify-center font-mono font-bold text-sm cursor-pointer transition-all hover:scale-110"
      style={{
        borderColor: `${color}60`,
        backgroundColor: `${color}15`,
        color,
        boxShadow: `0 0 8px ${color}30`,
      }}
    >
      {operation.gate === "MEASURE" ? "📏" : operation.gate.length <= 3 ? operation.gate : operation.gate.slice(0, 3)}
      <button
        onClick={(e) => { e.stopPropagation(); onRemove(operation.id); }}
        className="absolute -top-2 -right-2 w-4 h-4 rounded-full bg-red-500/80 text-white opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
      >
        <X className="w-2.5 h-2.5" />
      </button>
    </motion.div>
  );
}
