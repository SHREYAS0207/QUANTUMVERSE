export type GateType =
  | "H" | "X" | "Y" | "Z" | "S" | "T" | "SDG" | "TDG"
  | "RX" | "RY" | "RZ"
  | "CNOT" | "CX" | "CZ" | "SWAP" | "CCX"
  | "MEASURE" | "BARRIER";

export interface GateOperation {
  id: string;
  gate: GateType;
  targets: number[];
  controls: number[];
  column: number;
  params?: { angle?: number };
}

export interface Circuit {
  id: string;
  name: string;
  description?: string;
  qubits: number;
  classical_bits: number;
  circuit_data: {
    operations: GateOperation[];
  };
  is_template: boolean;
  template_name?: string;
  created_at: string;
  updated_at: string;
}

export interface SimulationResult {
  success: boolean;
  counts: Record<string, number>;
  probabilities: Record<string, number>;
  execution_time: number;
  total_shots: number;
  error?: string;
}

export interface StepResult {
  success: boolean;
  step_index: number;
  gate_applied: string;
  state_description: string;
  state_vector: [number, number][];
  probabilities: Record<string, number>;
  explanation: string;
  error?: string;
}

export interface GateInfo {
  type: GateType;
  label: string;
  color: string;
  description: string;
  category: "single" | "rotation" | "multi" | "measurement";
  requiresControl?: boolean;
  requiresParam?: boolean;
}
