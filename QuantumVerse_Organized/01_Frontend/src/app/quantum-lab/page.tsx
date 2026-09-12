"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Play,
  RotateCcw,
  Save,
  Minus,
  Plus,
  Undo2,
  Redo2,
  FlaskConical,
  Footprints,
  BarChart3,
  Sparkles,
  Atom,
  ChevronDown,
} from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { GatePalette } from "@/components/quantum-lab/GatePalette";
import { CircuitCanvas } from "@/components/quantum-lab/CircuitCanvas";
import { SimulationPanel } from "@/components/quantum-lab/SimulationPanel";
import { StepExecutor } from "@/components/quantum-lab/StepExecutor";
import { useCircuit } from "@/hooks/useCircuit";
import type { GateInfo } from "@/types/circuit";
import { cn } from "@/lib/utils";

const TEMPLATES = [
  {
    name: "Bell State",
    ops: [
      { gate: "H", targets: [0], controls: [], column: 0 },
      { gate: "CNOT", targets: [1], controls: [0], column: 1 },
      { gate: "MEASURE", targets: [0, 1], controls: [], column: 2 },
    ],
    qubits: 2,
    cb: 2,
  },
  {
    name: "Superposition",
    ops: [
      { gate: "H", targets: [0], controls: [], column: 0 },
      { gate: "MEASURE", targets: [0], controls: [], column: 1 },
    ],
    qubits: 1,
    cb: 1,
  },
  {
    name: "GHZ State",
    ops: [
      { gate: "H", targets: [0], controls: [], column: 0 },
      { gate: "CNOT", targets: [1], controls: [0], column: 1 },
      { gate: "CNOT", targets: [2], controls: [0], column: 2 },
      { gate: "MEASURE", targets: [0, 1, 2], controls: [], column: 3 },
    ],
    qubits: 3,
    cb: 3,
  },
  {
    name: "Phase Kickback",
    ops: [
      { gate: "H", targets: [0], controls: [], column: 0 },
      { gate: "X", targets: [1], controls: [], column: 0 },
      { gate: "CZ", targets: [1], controls: [0], column: 1 },
      { gate: "H", targets: [0], controls: [], column: 2 },
    ],
    qubits: 2,
    cb: 0,
  },
];

type PanelMode = "results" | "steps";

export default function QuantumLabPage() {
  const [selectedGate, setSelectedGate] = useState<GateInfo | null>(null);
  const [multiQubitStart, setMultiQubitStart] = useState<number | null>(null);
  const [panelMode, setPanelMode] = useState<PanelMode>("results");

  const circuit = useCircuit();

  const handleCellClick = (qubit: number, column: number) => {
    if (!selectedGate) return;

    const isMultiQubit = ["CNOT", "CX", "CZ", "SWAP"].includes(
      selectedGate.type
    );

    if (isMultiQubit) {
      if (multiQubitStart === null) {
        setMultiQubitStart(qubit);
        return;
      }

      if (multiQubitStart === qubit) {
        return;
      }

      circuit.addGate(
        selectedGate.type,
        [qubit],
        [multiQubitStart],
        column
      );

      setMultiQubitStart(null);
      return;
    }

    circuit.addGate(selectedGate.type, [qubit], [], column);
  };

  const handleLoadTemplate = (tpl: typeof TEMPLATES[number]) => {
    circuit.clearCircuit();
    circuit.setQubits(tpl.qubits);
    circuit.setClassicalBits(tpl.cb);

    tpl.ops.forEach((op) => {
      circuit.addGate(
        op.gate as any,
        op.targets,
        op.controls,
        op.column
      );
    });

    circuit.setCircuitName(tpl.name);
  };

  const maxStep = Math.max(
    ...circuit.operations.map((operation) => operation.column),
    0
  );

  return (
    <AppShell>
      {/* Page heading */}
      <div className="mb-5 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="mb-2 flex items-center gap-2 text-[10px] uppercase tracking-[0.25em] text-cyan-300/60">
            <Atom className="h-4 w-4" />
            Quantum Workspace
          </div>

          <h1 className="text-2xl font-bold tracking-tight text-white md:text-3xl">
            Quantum Circuit Lab
          </h1>

          <p className="mt-1 text-sm text-white/40">
            Build, simulate, and explore quantum circuits interactively.
          </p>
        </div>

        <div className="flex items-center gap-2 text-[10px] text-white/30">
          <Sparkles className="h-3.5 w-3.5 text-cyan-300/60" />
          Experiment freely — every circuit is simulated locally by the
          QuantumVerse backend.
        </div>
      </div>

      {/* Toolbar */}
      <div className="mb-4 rounded-2xl border border-white/10 bg-white/[0.025] p-3 backdrop-blur-xl">
        <div className="flex flex-wrap items-center gap-2">
          {/* Circuit name */}
          <div className="mr-1">
            <input
              value={circuit.circuitName}
              onChange={(event) =>
                circuit.setCircuitName(event.target.value)
              }
              className="w-44 rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-xs font-semibold text-white outline-none transition focus:border-cyan-400/40"
              placeholder="Circuit name"
            />
          </div>

          {/* Qubit control */}
          <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-black/30 px-3 py-1.5">
            <span className="text-[10px] uppercase tracking-wider text-white/30">
              Qubits
            </span>

            <button
              onClick={() => circuit.setQubits(circuit.qubits - 1)}
              disabled={circuit.qubits <= 1}
              className="flex h-6 w-6 items-center justify-center rounded-md text-white/40 transition hover:bg-white/10 hover:text-white disabled:opacity-30"
            >
              <Minus className="h-3 w-3" />
            </button>

            <span className="w-5 text-center font-mono text-sm font-bold text-cyan-300">
              {circuit.qubits}
            </span>

            <button
              onClick={() => circuit.setQubits(circuit.qubits + 1)}
              disabled={circuit.qubits >= 6}
              className="flex h-6 w-6 items-center justify-center rounded-md text-white/40 transition hover:bg-white/10 hover:text-white disabled:opacity-30"
            >
              <Plus className="h-3 w-3" />
            </button>
          </div>

          {/* History */}
          <div className="flex items-center rounded-xl border border-white/10 bg-black/30 p-1">
            <button
              onClick={circuit.undo}
              className="rounded-lg p-1.5 text-white/35 transition hover:bg-white/10 hover:text-white"
              title="Undo"
            >
              <Undo2 className="h-3.5 w-3.5" />
            </button>

            <button
              onClick={circuit.redo}
              className="rounded-lg p-1.5 text-white/35 transition hover:bg-white/10 hover:text-white"
              title="Redo"
            >
              <Redo2 className="h-3.5 w-3.5" />
            </button>

            <button
              onClick={circuit.clearCircuit}
              className="rounded-lg p-1.5 text-white/35 transition hover:bg-red-500/10 hover:text-red-300"
              title="Clear circuit"
            >
              <RotateCcw className="h-3.5 w-3.5" />
            </button>
          </div>

          {/* Template selector */}
          <div className="group relative">
            <button className="flex items-center gap-2 rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-xs text-white/55 transition hover:border-white/20 hover:text-white">
              Templates
              <ChevronDown className="h-3 w-3" />
            </button>

            <div className="invisible absolute left-0 top-full z-30 mt-2 w-48 rounded-xl border border-white/10 bg-black/95 p-1 opacity-0 shadow-2xl backdrop-blur-xl transition-all group-hover:visible group-hover:opacity-100">
              {TEMPLATES.map((tpl) => (
                <button
                  key={tpl.name}
                  onClick={() => handleLoadTemplate(tpl)}
                  className="flex w-full items-center rounded-lg px-3 py-2 text-left text-xs text-white/55 transition hover:bg-white/5 hover:text-cyan-300"
                >
                  {tpl.name}
                </button>
              ))}
            </div>
          </div>

          <div className="ml-auto flex items-center gap-2">
            <button
              onClick={circuit.saveCircuit}
              className="flex items-center gap-1.5 rounded-xl border border-white/10 bg-black/20 px-3 py-2 text-xs text-white/45 transition hover:border-white/20 hover:text-white"
            >
              <Save className="h-3.5 w-3.5" />
              Save
            </button>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={circuit.runSimulation}
              disabled={circuit.isSimulating}
              className="flex items-center gap-2 rounded-xl bg-cyan-400 px-5 py-2 text-xs font-bold text-black transition hover:bg-cyan-300 disabled:opacity-50"
            >
              {circuit.isSimulating ? (
                <>
                  <div className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-black/20 border-t-black" />
                  Simulating
                </>
              ) : (
                <>
                  <Play className="h-3.5 w-3.5" />
                  Run Circuit
                </>
              )}
            </motion.button>
          </div>
        </div>
      </div>

      {/* Workspace */}
      <div className="flex h-[calc(100vh-15rem)] min-h-[560px] overflow-hidden rounded-2xl border border-white/10 bg-black/40 shadow-2xl backdrop-blur-xl">
        {/* Gate Palette */}
        <GatePalette
          selectedGate={selectedGate}
          onGateSelect={(gate) =>
            setSelectedGate((previous) =>
              previous?.type === gate.type ? null : gate
            )
          }
        />

        {/* Circuit Canvas */}
        <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
          <div className="flex items-center justify-between border-b border-white/10 bg-white/[0.015] px-5 py-3">
            <div className="flex items-center gap-2 text-xs text-white/40">
              <FlaskConical className="h-3.5 w-3.5 text-cyan-300/70" />
              <span>{circuit.operations.length} operations</span>
              <span className="text-white/15">•</span>
              <span>{circuit.qubits} qubits</span>
            </div>

            {selectedGate ? (
              <span className="text-xs text-cyan-300/80">
                {["CNOT", "CX", "CZ", "SWAP"].includes(selectedGate.type)
                  ? multiQubitStart === null
                    ? `Select the first qubit for ${selectedGate.label}`
                    : `Select the second qubit for ${selectedGate.label}`
                  : `Click a cell to place ${selectedGate.label}`}
              </span>
            ) : (
              <span className="text-xs text-white/25">
                Select a gate from the palette to begin
              </span>
            )}
          </div>

          <CircuitCanvas
            qubits={circuit.qubits}
            operations={circuit.operations}
            columns={circuit.maxColumn}
            selectedGate={selectedGate}
            onCellClick={handleCellClick}
            onRemoveGate={circuit.removeGate}
            currentStep={circuit.currentStep}
            isStepping={circuit.isStepping}
          />
        </div>

        {/* Results */}
        <div className="flex w-72 shrink-0 flex-col overflow-hidden border-l border-white/10 bg-black/20">
          <div className="flex border-b border-white/10">
            {[
              {
                id: "results" as const,
                label: "Results",
                icon: BarChart3,
              },
              {
                id: "steps" as const,
                label: "Step Mode",
                icon: Footprints,
              },
            ].map((tab) => {
              const Icon = tab.icon;

              return (
                <button
                  key={tab.id}
                  onClick={() => setPanelMode(tab.id)}
                  className={cn(
                    "flex flex-1 items-center justify-center gap-1.5 border-b-2 py-3 text-[10px] font-medium uppercase tracking-wider transition-all",
                    panelMode === tab.id
                      ? "border-cyan-400 text-cyan-300"
                      : "border-transparent text-white/30 hover:text-white/70"
                  )}
                >
                  <Icon className="h-3.5 w-3.5" />
                  {tab.label}
                </button>
              );
            })}
          </div>

          <div className="flex-1 overflow-y-auto">
            {panelMode === "results" ? (
              <SimulationPanel result={circuit.simulationResult} />
            ) : (
              <StepExecutor
                maxStep={maxStep}
                currentStep={circuit.currentStep}
                stepResult={circuit.stepResult}
                isStepping={circuit.isStepping}
                onStep={(step) => circuit.runStep(step)}
                onReset={() => {
                  circuit.setCurrentStep(0);
                  circuit.setStepResult(null);
                }}
              />
            )}
          </div>
        </div>
      </div>
    </AppShell>
  );
}