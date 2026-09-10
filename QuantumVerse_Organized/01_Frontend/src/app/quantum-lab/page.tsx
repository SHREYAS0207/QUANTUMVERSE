"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import {
  Play, Pause, RotateCcw, Save, Minus, Plus, Undo2, Redo2,
  ChevronRight, FlaskConical, Footprints, BarChart3
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
  { name: "Bell State",    ops: [{gate:"H",targets:[0],controls:[],column:0},{gate:"CNOT",targets:[1],controls:[0],column:1},{gate:"MEASURE",targets:[0,1],controls:[],column:2}], qubits: 2, cb: 2 },
  { name: "Superposition", ops: [{gate:"H",targets:[0],controls:[],column:0},{gate:"MEASURE",targets:[0],controls:[],column:1}], qubits: 1, cb: 1 },
  { name: "GHZ State",     ops: [{gate:"H",targets:[0],controls:[],column:0},{gate:"CNOT",targets:[1],controls:[0],column:1},{gate:"CNOT",targets:[2],controls:[0],column:2},{gate:"MEASURE",targets:[0,1,2],controls:[],column:3}], qubits: 3, cb: 3 },
  { name: "Phase Kickback",ops: [{gate:"H",targets:[0],controls:[],column:0},{gate:"X",targets:[1],controls:[],column:0},{gate:"CZ",targets:[1],controls:[0],column:1},{gate:"H",targets:[0],controls:[],column:2}], qubits: 2, cb: 0 },
];

type PanelMode = "results" | "steps";

export default function QuantumLabPage() {
  const [
    selectedGate, setSelectedGate
  ] = useState<GateInfo | null>(null);
  const [multiQubitStart, setMultiQubitStart] = useState<number | null>(null);
  const [panelMode, setPanelMode] = useState<PanelMode>("results");
  const circuit = useCircuit();

  const handleCellClick = (qubit: number, column: number) => {
    if (!selectedGate) return;

    const isMultiQubit = ["CNOT", "CX", "CZ", "SWAP"].includes(selectedGate.type);

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

  const handleLoadTemplate = (tpl: typeof TEMPLATES[0]) => {
    circuit.clearCircuit();
    circuit.setQubits(tpl.qubits);
    circuit.setClassicalBits(tpl.cb);
    tpl.ops.forEach((op) => {
      circuit.addGate(op.gate as any, op.targets, op.controls, op.column);
    });
    circuit.setCircuitName(tpl.name);
  };

  const maxStep = Math.max(...circuit.operations.map((o) => o.column), 0);

  return (
    <AppShell>
      {/* Top toolbar */}
      <div className="flex items-center gap-3 mb-4 flex-wrap">
        {/* Circuit name */}
        <input
          value={circuit.circuitName}
          onChange={(e) => circuit.setCircuitName(e.target.value)}
          className="px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white font-medium focus:outline-none focus:border-quantum-blue/50 w-48"
        />

        {/* Qubits */}
        <div className="flex items-center gap-1.5 glass px-3 py-1.5 rounded-lg border border-white/5">
          <span className="text-xs text-muted-foreground">Qubits:</span>
          <button onClick={() => circuit.setQubits(circuit.qubits - 1)} disabled={circuit.qubits <= 1} className="w-5 h-5 rounded flex items-center justify-center hover:bg-white/10 disabled:opacity-40">
            <Minus className="w-3 h-3" />
          </button>
          <span className="text-sm font-mono text-quantum-blue w-4 text-center">{circuit.qubits}</span>
          <button onClick={() => circuit.setQubits(circuit.qubits + 1)} disabled={circuit.qubits >= 6} className="w-5 h-5 rounded flex items-center justify-center hover:bg-white/10 disabled:opacity-40">
            <Plus className="w-3 h-3" />
          </button>
        </div>

        {/* History controls */}
        <div className="flex gap-1">
          <button onClick={circuit.undo} className="p-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors" title="Undo">
            <Undo2 className="w-4 h-4" />
          </button>
          <button onClick={circuit.redo} className="p-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-white transition-colors" title="Redo">
            <Redo2 className="w-4 h-4" />
          </button>
          <button onClick={circuit.clearCircuit} className="p-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-red-400 transition-colors" title="Clear">
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>

        {/* Templates */}
        <div className="flex gap-1.5">
          {TEMPLATES.map((tpl) => (
            <button key={tpl.name} onClick={() => handleLoadTemplate(tpl)}
              className="px-3 py-1.5 rounded-lg text-xs border border-white/10 text-muted-foreground hover:border-quantum-blue/30 hover:text-white transition-all">
              {tpl.name}
            </button>
          ))}
        </div>

        <div className="ml-auto flex gap-2">
          <button onClick={circuit.saveCircuit} className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-white/10 text-xs text-muted-foreground hover:text-white hover:border-white/20 transition-all">
            <Save className="w-3.5 h-3.5" /> Save
          </button>
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={circuit.runSimulation}
            disabled={circuit.isSimulating}
            className="flex items-center gap-2 px-5 py-2 rounded-lg bg-quantum-blue text-quantum-dark font-bold text-sm hover:opacity-90 transition-opacity disabled:opacity-60"
          >
            {circuit.isSimulating ? (
              <><div className="w-3.5 h-3.5 border-2 border-quantum-dark/30 border-t-quantum-dark rounded-full animate-spin" /> Simulating...</>
            ) : (
              <><Play className="w-3.5 h-3.5" /> Run Circuit</>
            )}
          </motion.button>
        </div>
      </div>

      {/* Main layout */}
      <div className="flex gap-0 h-[calc(100vh-13rem)] rounded-xl overflow-hidden border border-white/5 glass">
        {/* Gate Palette */}
        <GatePalette selectedGate={selectedGate} onGateSelect={(g) => setSelectedGate((prev) => prev?.type === g.type ? null : g)} />

        {/* Circuit Canvas */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Canvas header */}
          <div className="px-5 py-3 border-b border-white/5 flex items-center gap-4">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <FlaskConical className="w-3.5 h-3.5" />
              <span>{circuit.operations.length} gates</span>
            </div>
            {selectedGate ? (
              <span className="text-xs text-quantum-blue">
                Click any empty cell to place <strong>{selectedGate.label}</strong> gate
              </span>
            ) : (
              <span className="text-xs text-muted-foreground">Select a gate from the palette, then click a cell</span>
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

        {/* Results Panel */}
        <div className="w-72 border-l border-white/5 flex flex-col overflow-hidden">
          {/* Panel tabs */}
          <div className="flex border-b border-white/5">
            {([
              { id: "results", label: "Results",    icon: BarChart3 },
              { id: "steps",   label: "Step Mode",  icon: Footprints },
            ] as const).map((tab) => (
              <button key={tab.id} onClick={() => setPanelMode(tab.id)}
                className={cn(
                  "flex-1 flex items-center justify-center gap-1.5 py-3 text-xs transition-all border-b-2",
                  panelMode === tab.id
                    ? "border-quantum-blue text-quantum-blue"
                    : "border-transparent text-muted-foreground hover:text-white"
                )}>
                <tab.icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            ))}
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
                onReset={() => { circuit.setCurrentStep(0); circuit.setStepResult(null); }}
              />
            )}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
