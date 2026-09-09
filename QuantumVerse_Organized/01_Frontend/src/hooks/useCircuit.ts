import { useCallback } from "react";
import { useCircuitStore } from "@/stores/circuitStore";
import { simulationService } from "@/services/simulationService";
import { circuitService } from "@/services/circuitService";
import toast from "react-hot-toast";
import type { GateType } from "@/types/circuit";

export function useCircuit() {
  const store = useCircuitStore();

  const runSimulation = useCallback(async () => {
    if (store.operations.length === 0) {
      toast.error("Add some gates before simulating!");
      return;
    }
    store.setIsSimulating(true);
    store.setSimulationResult(null);
    try {
      const result = await simulationService.run(
        store.qubits,
        store.operations,
        1024
      );
      store.setSimulationResult(result);
      if (result.success) {
        toast.success("Simulation complete!");
      } else {
        toast.error(result.error ?? "Simulation failed");
      }
    } catch {
      toast.error("Simulation error — check backend connection");
    } finally {
      store.setIsSimulating(false);
    }
  }, [store]);

  const runStep = useCallback(
    async (stepIndex: number) => {
      store.setIsStepping(true);
      try {
        const result = await simulationService.step(
          store.qubits,
          store.operations,
          stepIndex
        );
        store.setStepResult(result);
        store.setCurrentStep(stepIndex);
      } catch {
        toast.error("Step execution failed");
      } finally {
        store.setIsStepping(false);
      }
    },
    [store]
  );

  const saveCircuit = useCallback(async () => {
    try {
      await circuitService.create({
        name: store.circuitName,
        qubits: store.qubits,
        classical_bits: store.classicalBits,
        circuit_data: { operations: store.operations },
      } as any);
      toast.success("Circuit saved!");
    } catch {
      toast.error("Failed to save circuit");
    }
  }, [store]);

  const maxColumn = store.operations.length > 0
    ? Math.max(...store.operations.map((op) => op.column)) + 2
    : 8;

  return { ...store, runSimulation, runStep, saveCircuit, maxColumn };
}
