import api from "@/lib/api";
import type { SimulationResult, StepResult, GateOperation } from "@/types/circuit";

export const simulationService = {
  async run(qubits: number, operations: GateOperation[], shots = 1024, circuit_id?: string): Promise<SimulationResult> {
    const { data } = await api.post<SimulationResult>("/simulation/run", { qubits, operations, shots, circuit_id });
    return data;
  },
  async step(qubits: number, operations: GateOperation[], step_index: number): Promise<StepResult> {
    const { data } = await api.post<StepResult>("/simulation/step", { qubits, operations, step_index });
    return data;
  },
  async getHistory(): Promise<object[]> {
    const { data } = await api.get<{ history: object[] }>("/simulation/history");
    return data.history;
  },
};
