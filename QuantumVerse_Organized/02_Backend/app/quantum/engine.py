"""Core quantum circuit builder using Qiskit."""
from typing import Any
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter
import math


GATE_MAP = {
    "H":       lambda qc, t, c, p: qc.h(t[0]),
    "X":       lambda qc, t, c, p: qc.x(t[0]),
    "Y":       lambda qc, t, c, p: qc.y(t[0]),
    "Z":       lambda qc, t, c, p: qc.z(t[0]),
    "S":       lambda qc, t, c, p: qc.s(t[0]),
    "T":       lambda qc, t, c, p: qc.t(t[0]),
    "SDG":     lambda qc, t, c, p: qc.sdg(t[0]),
    "TDG":     lambda qc, t, c, p: qc.tdg(t[0]),
    "RX":      lambda qc, t, c, p: qc.rx(p.get("angle", math.pi / 2), t[0]),
    "RY":      lambda qc, t, c, p: qc.ry(p.get("angle", math.pi / 2), t[0]),
    "RZ":      lambda qc, t, c, p: qc.rz(p.get("angle", math.pi / 2), t[0]),
    "CNOT":    lambda qc, t, c, p: qc.cx(c[0], t[0]) if c else qc.cx(t[0], t[1]),
    "CX":      lambda qc, t, c, p: qc.cx(c[0], t[0]) if c else qc.cx(t[0], t[1]),
    "CZ":      lambda qc, t, c, p: qc.cz(c[0], t[0]) if c else qc.cz(t[0], t[1]),
    "SWAP":    lambda qc, t, c, p: qc.swap(t[0], t[1] if len(t) > 1 else t[0] + 1),
    "CCX":     lambda qc, t, c, p: qc.ccx(c[0], c[1] if len(c) > 1 else c[0] + 1, t[0]) if c else qc.ccx(t[0], t[1], t[2]),
    "MEASURE":  None,  # Handled specially
    "BARRIER": None,  # Handled specially
}


def build_circuit(qubits: int, classical_bits: int, operations: list[dict]) -> QuantumCircuit:
    """Build a Qiskit QuantumCircuit from a list of gate operations."""
    qr = QuantumRegister(qubits, "q")
    cb = ClassicalRegister(max(classical_bits, 1), "c")
    qc = QuantumCircuit(qr, cb)

    # Sort by column for ordered execution
    sorted_ops = sorted(operations, key=lambda o: o.get("column", 0))
    measure_ops = []

    for op in sorted_ops:
        gate = op.get("gate", "").upper()
        targets = [int(i) for i in op.get("targets", [])]
        controls = [int(i) for i in op.get("controls", [])]
        params = op.get("params") or {}

        # Validate qubit indices
        all_qubits = targets + controls
        if any(q >= qubits or q < 0 for q in all_qubits):
            continue

        if gate == "BARRIER":
            qc.barrier()
        elif gate == "MEASURE":
            measure_ops.extend(targets)
        elif gate in GATE_MAP and GATE_MAP[gate] is not None:
            try:
                GATE_MAP[gate](qc, targets, controls, params)
            except Exception:
                pass  # Skip malformed gates

    # Apply measurements at the end
    measured = set()
    for i, qubit in enumerate(measure_ops):
        if qubit < qubits and qubit not in measured:
            cbit = min(qubit, max(classical_bits, 1) - 1)
            qc.measure(qubit, cbit)
            measured.add(qubit)

    # If no explicit measurement, measure all
    if not measured:
        for i in range(qubits):
            cbit = min(i, max(classical_bits, 1) - 1)
            qc.measure(i, cbit)

    return qc


def circuit_to_dict(qc: QuantumCircuit) -> dict:
    """Return a simplified circuit descriptor for storage/display."""
    return {
        "num_qubits": qc.num_qubits,
        "num_clbits": qc.num_clbits,
        "depth": qc.depth(),
        "num_gates": len([inst for inst, _, _ in qc.data if inst.name != "measure"]),
        "qasm": qc.qasm() if hasattr(qc, "qasm") else str(qc),
    }
