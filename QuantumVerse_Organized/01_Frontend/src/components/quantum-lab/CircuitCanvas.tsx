"use client";

import { AnimatePresence, motion } from "framer-motion";
import { Crosshair, Layers3 } from "lucide-react";
import { GateBlock } from "./GateBlock";
import type { GateOperation, GateInfo } from "@/types/circuit";

interface CircuitCanvasProps {
  qubits: number;
  operations: GateOperation[];
  columns: number;
  selectedGate: GateInfo | null;
  onCellClick: (qubit: number, column: number) => void;
  onRemoveGate: (id: string) => void;
  currentStep: number;
  isStepping: boolean;
}

export function CircuitCanvas({
  qubits,
  operations,
  columns,
  selectedGate,
  onCellClick,
  onRemoveGate,
  currentStep,
  isStepping,
}: CircuitCanvasProps) {
  const getGateAt = (qubit: number, col: number) =>
    operations.find(
      (operation) =>
        operation.targets.includes(qubit) &&
        operation.column === col
    ) ||
    operations.find(
      (operation) =>
        operation.controls.includes(qubit) &&
        operation.column === col
    );

  const isColumnActive = (column: number) =>
    isStepping && column <= currentStep;

  return (
    <div className="relative flex-1 overflow-auto bg-[#030507]">
      {/* Atmospheric glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute left-1/3 top-1/4 h-72 w-72 rounded-full bg-cyan-400/[0.025] blur-3xl"
      />

      <div
        aria-hidden="true"
        className="pointer-events-none absolute bottom-0 right-0 h-64 w-64 rounded-full bg-violet-500/[0.02] blur-3xl"
      />

      {/* Technical grid */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 opacity-[0.025]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.5) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }}
      />

      <div className="relative min-w-max p-5 sm:p-7">
        {/* Canvas header */}
        <div className="mb-6 flex items-center justify-between gap-6 pl-[5rem]">
          <div className="flex items-center gap-3">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg border border-cyan-400/10 bg-cyan-400/[0.05]">
              <Layers3 className="h-3.5 w-3.5 text-cyan-300/70" />
            </div>

            <div>
              <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-white/45">
                Circuit workspace
              </p>
              <p className="mt-0.5 text-[9px] text-white/20">
                {operations.length} operation
                {operations.length === 1 ? "" : "s"} · {qubits} qubit
                {qubits === 1 ? "" : "s"}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {selectedGate && (
              <div className="hidden items-center gap-2 rounded-lg border border-cyan-400/10 bg-cyan-400/[0.035] px-2.5 py-1.5 sm:flex">
                <Crosshair className="h-3 w-3 text-cyan-300/60" />
                <span className="text-[9px] uppercase tracking-[0.12em] text-cyan-300/60">
                  Placement active
                </span>
              </div>
            )}

            <div className="flex items-center gap-2">
              <span
                className={`h-1.5 w-1.5 rounded-full ${
                  isStepping
                    ? "bg-amber-300 shadow-[0_0_9px_rgba(252,211,77,0.8)]"
                    : "bg-emerald-300 shadow-[0_0_9px_rgba(110,231,183,0.6)]"
                }`}
              />

              <span className="text-[9px] font-medium uppercase tracking-[0.14em] text-white/25">
                {isStepping
                  ? `Step ${currentStep} / ${Math.max(columns - 1, 0)}`
                  : "Ready"}
              </span>
            </div>
          </div>
        </div>

        {/* Circuit rows */}
        <div className="relative">
          {Array.from({ length: qubits }).map((_, qubit) => (
            <div
              key={qubit}
              className="group/row mb-3 flex items-center last:mb-0"
            >
              {/* Qubit identity */}
              <div className="w-[5rem] shrink-0 pr-4 text-right">
                <div className="inline-flex flex-col items-end">
                  <span className="font-mono text-[11px] font-semibold text-cyan-300/80">
                    q{qubit}
                  </span>

                  <span className="mt-1 font-mono text-[9px] text-white/20">
                    |0⟩
                  </span>
                </div>
              </div>

              {/* Circuit lane */}
              <div className="relative flex items-center">
                {/* Row hover */}
                <div
                  aria-hidden="true"
                  className="pointer-events-none absolute inset-x-0 h-14 rounded-xl bg-white/[0.018] opacity-0 transition-opacity duration-200 group-hover/row:opacity-100"
                />

                {Array.from({ length: columns }).map((_, col) => {
                  const gate = getGateAt(qubit, col);

                  const isControl = operations.some(
                    (operation) =>
                      operation.controls.includes(qubit) &&
                      operation.column === col
                  );

                  const active = isColumnActive(col);
                  const currentColumn =
                    isStepping && col === currentStep;

                  return (
                    <div
                      key={col}
                      className="relative flex h-14 w-16 shrink-0 items-center justify-center"
                    >
                      {/* Time column guide */}
                      <div
                        aria-hidden="true"
                        className={`pointer-events-none absolute inset-y-0 left-1/2 w-px -translate-x-1/2 transition-colors ${
                          currentColumn
                            ? "bg-amber-300/10"
                            : "bg-white/[0.018]"
                        }`}
                      />

                      {/* Active step column */}
                      {currentColumn && (
                        <motion.div
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          className="pointer-events-none absolute inset-y-1 left-1/2 w-12 -translate-x-1/2 rounded-xl border border-amber-300/10 bg-amber-300/[0.025]"
                        />
                      )}

                      {/* Quantum wire */}
                      <div
                        aria-hidden="true"
                        className={`absolute left-0 right-0 h-px transition-all duration-300 ${
                          active
                            ? "bg-gradient-to-r from-cyan-400/70 via-emerald-300/80 to-cyan-400/70 shadow-[0_0_8px_rgba(34,211,238,0.25)]"
                            : "bg-cyan-300/[0.14]"
                        }`}
                      />

                      {/* Cell interaction */}
                      <div
                        className="relative z-10 flex h-14 w-16 items-center justify-center"
                        onClick={() =>
                          !gate && onCellClick(qubit, col)
                        }
                      >
                        {gate ? (
                          isControl ? (
                            <div className="relative flex h-7 w-7 items-center justify-center">
                              <div className="absolute h-6 w-6 rounded-full border border-cyan-300/15" />

                              <div className="h-2.5 w-2.5 rounded-full bg-cyan-300 shadow-[0_0_12px_rgba(103,232,249,0.8)]" />
                            </div>
                          ) : (
                            <AnimatePresence>
                              <GateBlock
                                key={gate.id}
                                operation={gate}
                                onRemove={onRemoveGate}
                              />
                            </AnimatePresence>
                          )
                        ) : (
                          <button
                            type="button"
                            aria-label={`Place gate on q${qubit}, time ${col}`}
                            onClick={() =>
                              onCellClick(qubit, col)
                            }
                            className={[
                              "flex h-10 w-12 items-center justify-center rounded-lg",
                              "border border-dashed transition-all duration-200",
                              selectedGate
                                ? "border-cyan-300/15 bg-cyan-300/[0.012] text-cyan-300/20 hover:border-cyan-300/55 hover:bg-cyan-300/[0.055] hover:text-cyan-300/70"
                                : "border-transparent text-transparent hover:border-white/[0.08] hover:bg-white/[0.02]",
                            ].join(" ")}
                          >
                            {selectedGate && (
                              <span className="text-sm font-medium">+</span>
                            )}
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}

                {/* Wire terminator */}
                <div className="relative h-14 w-10 shrink-0">
                  <div
                    className={`absolute left-0 right-2 top-1/2 h-px ${
                      isStepping
                        ? "bg-cyan-300/25"
                        : "bg-cyan-300/10"
                    }`}
                  />

                  <div className="absolute right-0 top-1/2 h-1.5 w-1.5 -translate-y-1/2 rounded-full bg-cyan-300/30" />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Timeline */}
        <div className="mt-5 flex items-center pl-[5rem]">
          <div className="mr-2 w-5 text-[8px] font-medium uppercase tracking-[0.12em] text-white/15">
            time
          </div>

          {Array.from({ length: columns }).map((_, col) => {
            const active =
              isStepping && col === currentStep;

            return (
              <div
                key={col}
                className="flex h-7 w-16 shrink-0 items-center justify-center"
              >
                <span
                  className={[
                    "rounded-md border px-1.5 py-0.5 font-mono text-[8px] transition-all",
                    active
                      ? "border-amber-300/15 bg-amber-300/[0.08] text-amber-200"
                      : "border-transparent text-white/20",
                  ].join(" ")}
                >
                  t{col}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}