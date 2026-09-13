"""Qiskit Aer simulation engine."""
import time
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from .engine import build_circuit

_SIM = AerSimulator()


def run_simulation(qubits: int, classical_bits: int, operations: list[dict], shots: int = 1024) -> dict:
    """Run a statevector + shot-based simulation and return counts + probabilities."""
    start = time.perf_counter()

    try:
        qc = build_circuit(qubits, classical_bits, operations)
        job = _SIM.run(qc, shots=shots)
        result = job.result()
        counts: dict[str, int] = result.get_counts(0)
        total = sum(counts.values())
        probabilities = {state: count / total for state, count in counts.items()}
        execution_time = round((time.perf_counter() - start) * 1000, 2)

        return {
            "success": True,
            "counts": counts,
            "probabilities": probabilities,
            "execution_time": execution_time,
            "total_shots": total,
        }
    except Exception as exc:
        return {
            "success": False,
            "counts": {},
            "probabilities": {},
            "execution_time": 0,
            "total_shots": 0,
            "error": str(exc),
        }


def run_statevector(qubits: int, operations: list[dict]) -> dict:
    """Run a statevector simulation (no measurement) and return state amplitudes."""
    sv_sim = AerSimulator(method="statevector")

    # Build circuit WITHOUT measurement for statevector
    from qiskit import QuantumRegister, ClassicalRegister
    from .engine import GATE_MAP
    import math

    qr = QuantumRegister(qubits, "q")
    qc = QuantumCircuit(qr)
    sorted_ops = sorted(
        [o for o in operations if o.get("gate", "").upper() not in ("MEASURE", "BARRIER")],
        key=lambda o: o.get("column", 0),
    )

    for op in sorted_ops:
        gate = op.get("gate", "").upper()
        targets = [int(i) for i in op.get("targets", [])]
        controls = [int(i) for i in op.get("controls", [])]
        params = op.get("params") or {}
        all_qubits = targets + controls
        if any(q >= qubits or q < 0 for q in all_qubits):
            continue
        if gate in GATE_MAP and GATE_MAP[gate] is not None:
            try:
                GATE_MAP[gate](qc, targets, controls, params)
            except Exception:
                pass

    try:
        qc.save_state()
        job = sv_sim.run(qc)
        sv = job.result().get_statevector(0)
        statevector = np.asarray(sv)
        amps = [(float(a.real), float(a.imag)) for a in statevector]
        probs = {format(i, f"0{qubits}b"): abs(a) ** 2 for i, a in enumerate(statevector)}
        probs = {k: round(v, 6) for k, v in probs.items() if v > 1e-8}
        return {"success": True, "state_vector": amps, "probabilities": probs}
    except Exception as exc:
        return {"success": False, "error": str(exc), "state_vector": [], "probabilities": {}}
