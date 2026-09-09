"use client";
import { motion } from "framer-motion";
import { GATE_CATALOG } from "@/lib/constants";
import type { GateType, GateInfo } from "@/types/circuit";

interface GatePaletteProps {
  onGateSelect: (gate: GateInfo) => void;
  selectedGate: GateInfo | null;
}

const CATEGORIES = [
  { id: "single",      label: "Single Qubit" },
  { id: "rotation",   label: "Rotation" },
  { id: "multi",      label: "Multi-Qubit" },
  { id: "measurement",label: "Measurement" },
];

export function GatePalette({ onGateSelect, selectedGate }: GatePaletteProps) {
  return (
    <div className="w-52 glass border-r border-quantum-blue/10 p-3 overflow-y-auto flex-shrink-0">
      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-widest mb-4 px-1">Gate Palette</p>
      {CATEGORIES.map((cat) => {
        const gates = GATE_CATALOG.filter((g) => g.category === cat.id);
        if (!gates.length) return null;
        return (
          <div key={cat.id} className="mb-5">
            <p className="text-[10px] text-muted-foreground uppercase tracking-wider mb-2 px-1">{cat.label}</p>
            <div className="grid grid-cols-2 gap-1.5">
              {gates.map((gate) => (
                <motion.button
                  key={gate.type}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => onGateSelect(gate)}
                  title={gate.description}
                  className={`relative flex flex-col items-center justify-center px-2 py-2.5 rounded-lg border text-xs font-bold font-mono transition-all ${
                    selectedGate?.type === gate.type
                      ? "border-quantum-blue/60 bg-quantum-blue/20 text-quantum-blue"
                      : "border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/10"
                  }`}
                  style={selectedGate?.type === gate.type ? {} : { color: gate.color }}
                >
                  <span className="text-sm" style={{ color: gate.color }}>{gate.label}</span>
                  <span className="text-[9px] text-muted-foreground mt-0.5 truncate w-full text-center">{gate.description.split("—")[0].trim()}</span>
                  {selectedGate?.type === gate.type && (
                    <div className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-quantum-blue" />
                  )}
                </motion.button>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
