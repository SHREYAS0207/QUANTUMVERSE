"use client";
import { AnimatePresence } from "framer-motion";
import { GateBlock } from "./GateBlock";
import type { GateOperation } from "@/types/circuit";
import type { GateInfo } from "@/types/circuit";

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
    operations.find((op) => op.targets.includes(qubit) && op.column === col) ||
    operations.find((op) => op.controls.includes(qubit) && op.column === col);

  return (
    <div className="flex-1 overflow-auto p-6">
      <div className="min-w-max">
        {Array.from({ length: qubits }).map((_, qubit) => (
          <div key={qubit} className="flex items-center mb-4">
            {/* Qubit label */}
            <div className="w-14 flex-shrink-0 text-right pr-3">
              <span className="text-xs font-mono text-quantum-blue">q{qubit}</span>
              <span className="block text-[9px] text-muted-foreground font-mono">|0⟩</span>
            </div>

            {/* Wire + cells */}
            <div className="flex items-center">
              {Array.from({ length: columns }).map((_, col) => {
                const gate = getGateAt(qubit, col);
                const isControl = operations.some(
                  (op) => op.controls.includes(qubit) && op.column === col
                );
                const isActiveStep = isStepping && col <= currentStep;

                return (
                  <div key={col} className="relative flex items-center">
                    {/* Wire segment */}
                    <div
                      className="h-px w-12"
                      style={{
                        background: isActiveStep
                          ? "linear-gradient(90deg, #00D4FF, #06FFA5)"
                          : "rgba(0,212,255,0.2)",
                        boxShadow: isActiveStep ? "0 0 6px rgba(0,212,255,0.4)" : undefined,
                      }}
                    />

                    {/* Cell */}
                    <div
                      className="relative flex items-center justify-center w-12 h-12 cursor-pointer"
                      onClick={() => !gate && onCellClick(qubit, col)}
                    >
                      {gate ? (
                        isControl ? (
                          // Control dot
                          <div className="w-3 h-3 rounded-full bg-quantum-blue border-2 border-quantum-blue shadow-[0_0_8px_rgba(0,212,255,0.6)]" />
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
                        // Empty cell hover effect
                        <div className={`w-10 h-10 rounded-lg border border-dashed transition-all ${
                          selectedGate
                            ? "border-quantum-blue/30 hover:border-quantum-blue/70 hover:bg-quantum-blue/5"
                            : "border-transparent"
                        }`} />
                      )}
                    </div>
                  </div>
                );
              })}

              {/* End wire */}
              <div className="h-px w-8 bg-quantum-blue/20" />
              <div className="w-2 h-2 rounded-full bg-quantum-blue/40" />
            </div>
          </div>
        ))}

        {/* Column step indicators */}
        <div className="flex items-center ml-14">
          {Array.from({ length: columns }).map((_, col) => (
            <div key={col} className="flex items-center">
              <div className="w-12" />
              <div className="w-12 text-center">
                <span className={`text-[9px] font-mono ${
                  isStepping && col === currentStep ? "text-quantum-blue" : "text-muted-foreground/40"
                }`}>t{col}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
