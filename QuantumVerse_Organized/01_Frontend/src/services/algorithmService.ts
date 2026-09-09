import api from "@/lib/api";

export const algorithmService = {
  async list(): Promise<object[]> {
    const { data } = await api.get<{ algorithms: object[] }>("/algorithms");
    return data.algorithms;
  },
  async runGrover(n_qubits: number, target: number, iterations?: number): Promise<object> {
    const { data } = await api.post("/algorithms/grover/run", { n_qubits, target, iterations });
    return data;
  },
  async runTeleportation(state: string): Promise<object> {
    const { data } = await api.post("/algorithms/teleportation/run", { state });
    return data;
  },
  async runDeutschJozsa(oracle_type: string, n_qubits: number): Promise<object> {
    const { data } = await api.post("/algorithms/deutsch-jozsa/run", { oracle_type, n_qubits });
    return data;
  },
  async runQFT(n_qubits: number, input_state: number): Promise<object> {
    const { data } = await api.post("/algorithms/qft/run", { n_qubits, input_state });
    return data;
  },
};
