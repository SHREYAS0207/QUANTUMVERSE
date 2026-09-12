"use client";

import { motion } from "framer-motion";
import {
  Atom,
  CircleDot,
  GitBranch,
  RotateCw,
  ScanLine,
} from "lucide-react";
import { GATE_CATALOG } from "@/lib/constants";
import type { GateInfo } from "@/types/circuit";

interface GatePaletteProps {
  onGateSelect: (gate: GateInfo) => void;
  selectedGate: GateInfo | null;
}

const CATEGORIES = [
  {
    id: "single",
    label: "Single Qubit",
    icon: Atom,
  },
  {
    id: "rotation",
    label: "Rotation",
    icon: RotateCw,
  },
  {
    id: "multi",
    label: "Multi-Qubit",
    icon: GitBranch,
  },
  {
    id: "measurement",
    label: "Measurement",
    icon: ScanLine,
  },
];

export function GatePalette({
  onGateSelect,
  selectedGate,
}: GatePaletteProps) {
  return (
    <aside className="flex w-56 shrink-0 flex-col overflow-hidden border-r border-white/10 bg-black/25">
      {/* Header */}
      <div className="border-b border-white/10 px-4 py-4">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg border border-cyan-400/20 bg-cyan-400/10">
            <Atom className="h-3.5 w-3.5 text-cyan-300" />
          </div>

          <div>
            <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-white/80">
              Gate Palette
            </p>
            <p className="mt-0.5 text-[9px] text-white/25">
              Select an operation
            </p>
          </div>
        </div>
      </div>

      {/* Gate list */}
      <div className="flex-1 overflow-y-auto px-3 py-4">
        {CATEGORIES.map((category) => {
          const gates = GATE_CATALOG.filter(
            (gate) => gate.category === category.id
          );

          if (!gates.length) return null;

          const CategoryIcon = category.icon;

          return (
            <section key={category.id} className="mb-5">
              {/* Category label */}
              <div className="mb-2 flex items-center gap-2 px-1">
                <CategoryIcon className="h-3 w-3 text-white/25" />

                <span className="text-[9px] font-semibold uppercase tracking-[0.16em] text-white/30">
                  {category.label}
                </span>

                <div className="h-px flex-1 bg-white/5" />
              </div>

              {/* Gates */}
              <div className="grid grid-cols-2 gap-1.5">
                {gates.map((gate) => {
                  const isSelected = selectedGate?.type === gate.type;

                  return (
                    <motion.button
                      key={gate.type}
                      whileHover={{ y: -1 }}
                      whileTap={{ scale: 0.96 }}
                      onClick={() => onGateSelect(gate)}
                      title={gate.description}
                      className={`
                        group relative flex min-h-[68px] flex-col items-center
                        justify-center overflow-hidden rounded-xl border
                        px-2 py-2 transition-all
                        ${
                          isSelected
                            ? "border-cyan-400/50 bg-cyan-400/[0.09] shadow-[0_0_20px_rgba(34,211,238,0.08)]"
                            : "border-white/[0.08] bg-white/[0.025] hover:border-white/15 hover:bg-white/[0.055]"
                        }
                      `}
                    >
                      {/* Active background */}
                      {isSelected && (
                        <motion.div
                          layoutId="selected-gate"
                          className="absolute inset-0 bg-gradient-to-br from-cyan-400/[0.08] to-transparent"
                        />
                      )}

                      {/* Gate symbol */}
                      <span
                        className="relative z-10 font-mono text-base font-bold transition-transform group-hover:scale-105"
                        style={{
                          color: isSelected ? "#67e8f9" : gate.color,
                        }}
                      >
                        {gate.label}
                      </span>

                      {/* Gate description */}
                      <span
                        className={`
                          relative z-10 mt-1 w-full truncate text-center text-[8px]
                          ${
                            isSelected
                              ? "text-cyan-200/50"
                              : "text-white/25"
                          }
                        `}
                      >
                        {gate.description.split("—")[0].trim()}
                      </span>

                      {/* Selected indicator */}
                      {isSelected && (
                        <>
                          <div className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-cyan-300 shadow-[0_0_8px_rgba(103,232,249,0.8)]" />

                          <div className="absolute bottom-0 left-1/2 h-px w-8 -translate-x-1/2 bg-cyan-300/60" />
                        </>
                      )}
                    </motion.button>
                  );
                })}
              </div>
            </section>
          );
        })}
      </div>

      {/* Selection status */}
      <div className="border-t border-white/10 bg-black/20 p-3">
        {selectedGate ? (
          <div className="rounded-xl border border-cyan-400/15 bg-cyan-400/[0.04] p-3">
            <div className="mb-1.5 flex items-center gap-2">
              <CircleDot className="h-3 w-3 text-cyan-300" />

              <span className="text-[9px] font-semibold uppercase tracking-[0.15em] text-cyan-300/70">
                Selected
              </span>
            </div>

            <div className="flex items-center gap-2">
              <span
                className="font-mono text-lg font-bold"
                style={{ color: selectedGate.color }}
              >
                {selectedGate.label}
              </span>

              <span className="truncate text-[9px] text-white/35">
                {selectedGate.description.split("—")[0].trim()}
              </span>
            </div>
          </div>
        ) : (
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-3">
            <p className="text-[9px] uppercase tracking-[0.12em] text-white/20">
              No gate selected
            </p>

            <p className="mt-1 text-[9px] leading-relaxed text-white/30">
              Choose a gate, then click a circuit cell to place it.
            </p>
          </div>
        )}
      </div>
    </aside>
  );
}