"use client";

import { AnimatePresence } from "framer-motion";
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
    <div className="relative flex-1 overflow-auto bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.025),transparent_55%)] p-6">
      {/* Subtle technical grid */}
      <div className="pointer-events-none absolute inset-0 opacity-[0.035] [background-image:linear-gradient(rgba(255,255,255,.5)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.5)_1px,transparent_1px)] [background-size:32px_32px]" />

      <div className="relative min-w-max">
        {/* Circuit status */}
        <div className="mb-5 flex items-center gap-3 pl-[4.5rem]">
          <div className="flex items-center gap-2">
            <span
              className={`h-1.5 w-1.5 rounded-full ${
                isStepping
                  ? "bg-yellow-300 shadow-[0_0_8px_rgba(253,224,71,.7)]"
                  : "bg-cyan-300 shadow-[0_0_8px_rgba(103,232,249,.5)]"
              }`}
            />

            <span className="text-[9px] uppercase tracking-[0.18em] text-white/25">
              {isStepping
                ? `Step ${currentStep} / ${Math.max(columns - 1, 0)}`
                : "Circuit ready"}
            </span>
          </div>

          <div className="h-px w-12 bg-white/5" />

          <span className="text-[9px] text-white/20">
            {operations.length} operation
            {operations.length === 1 ? "" : "s"}
          </span>
        </div>

        {/* Qubit rows */}
        {Array.from({ length: qubits }).map((_, qubit) => (
          <div
            key={qubit}
            className="group/row mb-4 flex items-center"
          >
            {/* Qubit label */}
            <div className="w-[4.5rem] shrink-0 pr-4 text-right">
              <div className="font-mono text-xs font-semibold text-cyan-300/80">
                q{qubit}
              </div>

              <div className="mt-0.5 font-mono text-[9px] text-white/25">
                |0⟩
              </div>
            </div>

            {/* Circuit lane */}
            <div className="relative flex items-center">
              {/* Row hover highlight */}
              <div className="pointer-events-none absolute inset-x-0 h-12 rounded-xl bg-white/[0.012] opacity-0 transition-opacity group-hover/row:opacity-100" />

              {Array.from({ length: columns }).map((_, col) => {
                const gate = getGateAt(qubit, col);

                const isControl = operations.some(
                  (operation) =>
                    operation.controls.includes(qubit) &&
                    operation.column === col
                );

                const active = isColumnActive(col);

                return (
                  <div
                    key={col}
                    className="relative flex h-12 w-16 shrink-0 items-center"
                  >
                    {/* Quantum wire */}
                    <div
                      className={`absolute left-0 right-0 h-px transition-all ${
                        active
                          ? "bg-gradient-to-r from-cyan-400 via-emerald-300 to-cyan-400 shadow-[0_0_7px_rgba(34,211,238,.35)]"
                          : "bg-cyan-300/15"
                      }`}
                    />

                    {/* Active step column */}
                    {isStepping && col === currentStep && (
                      <div className="pointer-events-none absolute inset-y-0 left-1/2 w-12 -translate-x-1/2 rounded-lg border border-yellow-300/10 bg-yellow-300/[0.025]" />
                    )}

                    {/* Cell */}
                    <div
                      className="relative z-10 flex h-12 w-16 items-center justify-center"
                      onClick={() =>
                        !gate && onCellClick(qubit, col)
                      }
                    >
                      {gate ? (
                        isControl ? (
                          /* Control dot */
                          <div className="relative flex h-6 w-6 items-center justify-center">
                            <div className="absolute h-5 w-5 rounded-full border border-cyan-300/20" />

                            <div className="h-2.5 w-2.5 rounded-full bg-cyan-300 shadow-[0_0_10px_rgba(103,232,249,.7)]" />
                          </div>
                        ) : (
                          /* Gate */
                          <AnimatePresence>
                            <GateBlock
                              key={gate.id}
                              operation={gate}
                              onRemove={onRemoveGate}
                            />
                          </AnimatePresence>
                        )
                      ) : (
                        /* Empty placement cell */
                        <button
                          type="button"
                          aria-label={`Place gate on q${qubit}, time ${col}`}
                          onClick={() =>
                            onCellClick(qubit, col)
                          }
                          className={`
                            h-9 w-11 rounded-lg border border-dashed
                            transition-all
                            ${
                              selectedGate
                                ? "border-cyan-300/20 bg-cyan-300/[0.015] hover:border-cyan-300/60 hover:bg-cyan-300/[0.06]"
                                : "border-transparent hover:border-white/10 hover:bg-white/[0.025]"
                            }
                          `}
                        >
                          {selectedGate && (
                            <span className="text-[10px] text-cyan-300/20">
                              +
                            </span>
                          )}
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}

              {/* End of quantum wire */}
              <div className="relative h-12 w-10 shrink-0">
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

        {/* Timeline */}
        <div className="mt-2 flex items-center pl-[4.5rem]">
          {Array.from({ length: columns }).map((_, col) => {
            const active =
              isStepping && col === currentStep;

            return (
              <div
                key={col}
                className="flex h-7 w-16 shrink-0 items-center justify-center"
              >
                <span
                  className={`rounded-md px-1.5 py-0.5 font-mono text-[8px] transition-all ${
                    active
                      ? "bg-yellow-300/10 text-yellow-200"
                      : "text-white/20"
                  }`}
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