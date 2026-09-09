import { create } from "zustand";
import { v4 as uuidv4 } from "uuid";
import type { GateOperation, GateType, SimulationResult, StepResult } from "@/types/circuit";

interface CircuitState {
  qubits: number;
  classicalBits: number;
  operations: GateOperation[];
  history: GateOperation[][];
  historyIndex: number;
  simulationResult: SimulationResult | null;
  stepResult: StepResult | null;
  currentStep: number;
  isSimulating: boolean;
  isStepping: boolean;
  circuitName: string;

  setQubits: (n: number) => void;
  setClassicalBits: (n: number) => void;
  addGate: (gate: GateType, targets: number[], controls: number[], column: number, params?: object) => void;
  removeGate: (id: string) => void;
  moveGate: (id: string, newColumn: number, newTarget: number) => void;
  clearCircuit: () => void;
  undo: () => void;
  redo: () => void;
  setSimulationResult: (result: SimulationResult | null) => void;
  setStepResult: (result: StepResult | null) => void;
  setCurrentStep: (step: number) => void;
  setIsSimulating: (v: boolean) => void;
  setIsStepping: (v: boolean) => void;
  setCircuitName: (name: string) => void;
  loadCircuit: (ops: GateOperation[], qubits: number, classicalBits: number) => void;
}

export const useCircuitStore = create<CircuitState>((set, get) => ({
  qubits: 2,
  classicalBits: 2,
  operations: [],
  history: [[]],
  historyIndex: 0,
  simulationResult: null,
  stepResult: null,
  currentStep: 0,
  isSimulating: false,
  isStepping: false,
  circuitName: "My Circuit",

  setQubits: (n) => set({ qubits: Math.max(1, Math.min(6, n)) }),
  setClassicalBits: (n) => set({ classicalBits: Math.max(0, Math.min(6, n)) }),

  addGate: (gate, targets, controls, column, params) => {
    const newOp: GateOperation = { id: uuidv4(), gate, targets, controls, column, params };
    set((state) => {
      const newOps = [...state.operations, newOp];
      const newHistory = state.history.slice(0, state.historyIndex + 1);
      newHistory.push(newOps);
      return { operations: newOps, history: newHistory, historyIndex: newHistory.length - 1 };
    });
  },

  removeGate: (id) => {
    set((state) => {
      const newOps = state.operations.filter((op) => op.id !== id);
      const newHistory = state.history.slice(0, state.historyIndex + 1);
      newHistory.push(newOps);
      return { operations: newOps, history: newHistory, historyIndex: newHistory.length - 1 };
    });
  },

  moveGate: (id, newColumn, newTarget) => {
    set((state) => {
      const newOps = state.operations.map((op) =>
        op.id === id ? { ...op, column: newColumn, targets: [newTarget] } : op
      );
      return { operations: newOps };
    });
  },

  clearCircuit: () => {
    set((state) => ({
      operations: [],
      history: [[]],
      historyIndex: 0,
      simulationResult: null,
      stepResult: null,
    }));
  },

  undo: () => {
    set((state) => {
      if (state.historyIndex <= 0) return state;
      const newIndex = state.historyIndex - 1;
      return { operations: state.history[newIndex], historyIndex: newIndex };
    });
  },

  redo: () => {
    set((state) => {
      if (state.historyIndex >= state.history.length - 1) return state;
      const newIndex = state.historyIndex + 1;
      return { operations: state.history[newIndex], historyIndex: newIndex };
    });
  },

  setSimulationResult: (result) => set({ simulationResult: result }),
  setStepResult: (result) => set({ stepResult: result }),
  setCurrentStep: (step) => set({ currentStep: step }),
  setIsSimulating: (v) => set({ isSimulating: v }),
  setIsStepping: (v) => set({ isStepping: v }),
  setCircuitName: (name) => set({ circuitName: name }),
  loadCircuit: (ops, qubits, classicalBits) =>
    set({ operations: ops, qubits, classicalBits, history: [ops], historyIndex: 0 }),
}));
