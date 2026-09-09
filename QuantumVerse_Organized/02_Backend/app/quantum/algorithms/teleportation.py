"""Quantum Teleportation circuit."""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


STATE_GATES = {
    "zero":  [],
    "one":   [("x", 0)],
    "plus":  [("h", 0)],
    "minus": [("x", 0), ("h", 0)],
}


def run_teleportation(state: str = "plus") -> dict:
    """Teleport qubit 0 to qubit 2 using entanglement."""
    state = state if state in STATE_GATES else "plus"
    qc = QuantumCircuit(3, 3)

    # Prepare state to teleport
    for gate, qubit in STATE_GATES[state]:
        getattr(qc, gate)(qubit)

    qc.barrier()

    # Create Bell pair between qubits 1 and 2
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()

    # Bell measurement on qubits 0 and 1
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()
    qc.measure(0, 0)
    qc.measure(1, 1)

    # Conditional corrections
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(2)
    with qc.if_test((qc.clbits[0], 1)):
        qc.z(2)

    qc.measure(2, 2)

    sim = AerSimulator()
    counts = sim.run(qc, shots=1024).result().get_counts(0)
    total = sum(counts.values())

    # Qubit 2 (rightmost bit in Qiskit's ordering) should match original
    qubit2_counts = {"0": 0, "1": 0}
    for state_str, count in counts.items():
        qubit2_counts[state_str[0]] += count  # leftmost char = qubit 2

    return {
        "algorithm": "teleportation",
        "initial_state": state,
        "counts": counts,
        "qubit_2_outcome": {k: round(v / total, 4) for k, v in qubit2_counts.items()},
        "probabilities": {k: round(v / total, 4) for k, v in counts.items()},
        "steps": [
            {"step": 1, "description": f"Prepared qubit 0 in |{state}⟩ state"},
            {"step": 2, "description": "Created Bell pair |Φ+⟩ between qubits 1 and 2"},
            {"step": 3, "description": "Performed Bell measurement on sender qubits 0 and 1"},
            {"step": 4, "description": "Applied classical corrections on receiver (qubit 2)"},
            {"step": 5, "description": "Teleportation complete — qubit state transferred!"},
        ],
        "success": True,
    }
