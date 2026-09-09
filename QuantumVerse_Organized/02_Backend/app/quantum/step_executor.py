"""Step-by-step gate execution with explanations."""
from .simulator import run_statevector

GATE_EXPLANATIONS = {
    "H":    "Hadamard gate — puts qubit into equal superposition. |0⟩ → ½(|0⟩+|1⟩), |1⟩ → ½(|0⟩-|1⟩).",
    "X":    "Pauli-X (NOT) gate — flips qubit state: |0⟩ → |1⟩ and |1⟩ → |0⟩.",
    "Y":    "Pauli-Y gate — combines X and Z rotations with an imaginary phase factor.",
    "Z":    "Pauli-Z gate — phase flip: |0⟩ unchanged, |1⟩ → -|1⟩. No visible effect until interference.",
    "S":    "S gate (√Z) — applies a 90° phase rotation to |1⟩. Used in QFT.",
    "T":    "T gate (√S) — applies a 45° phase rotation. Important for universal quantum computing.",
    "SDG":  "S-dagger — inverse S gate, -90° phase rotation.",
    "TDG":  "T-dagger — inverse T gate, -45° phase rotation.",
    "RX":   "Rotation around X-axis by angle θ. Generalization of the X gate.",
    "RY":   "Rotation around Y-axis. Used to create arbitrary superpositions.",
    "RZ":   "Rotation around Z-axis. Applies a relative phase without changing probabilities.",
    "CNOT": "Controlled-NOT — flips target qubit only when control is |1⟩. Creates entanglement!",
    "CX":   "Controlled-X (same as CNOT). The workhorse two-qubit gate.",
    "CZ":   "Controlled-Z — applies Z to target when control is |1⟩. Symmetric in effect.",
    "SWAP": "SWAP — exchanges two qubit states completely.",
    "CCX":  "Toffoli (CCX) — flips target when both controls are |1⟩. Reversible NAND.",
    "MEASURE": "Measurement — collapses superposition to |0⟩ or |1⟩ with Born-rule probabilities.",
    "BARRIER": "Barrier — visual/compilation separator. No physical effect.",
}


def format_state_description(probabilities: dict, qubits: int) -> str:
    """Return a human-readable state description."""
    dominant = [(s, p) for s, p in probabilities.items() if p > 0.001]
    dominant.sort(key=lambda x: -x[1])
    if not dominant:
        return "|0⟩" * qubits
    if len(dominant) == 1:
        return f"|{dominant[0][0]}⟩"
    parts = " + ".join(
        f"{round(p**0.5, 2)}|{s}⟩" for s, p in dominant[:4]
    )
    return parts


def execute_step(qubits: int, operations: list[dict], step_index: int) -> dict:
    """Execute circuit up to step_index and return state info."""
    sorted_ops = sorted(operations, key=lambda o: o.get("column", 0))
    non_measure = [o for o in sorted_ops if o.get("gate", "").upper() not in ("MEASURE", "BARRIER")]

    target_step = min(step_index, len(non_measure) - 1)
    ops_so_far = non_measure[: target_step + 1]

    if not ops_so_far:
        return {
            "success": True, "step_index": step_index,
            "gate_applied": "INIT", "state_description": f"|{'0' * qubits}⟩",
            "state_vector": [(1.0, 0.0)] + [(0.0, 0.0)] * (2 ** qubits - 1),
            "probabilities": {"0" * qubits: 1.0},
            "explanation": f"Initial state: all {qubits} qubits in |0⟩.",
        }

    gate_applied = ops_so_far[-1].get("gate", "?").upper()
    sv_result = run_statevector(qubits, ops_so_far)

    if not sv_result.get("success"):
        return {"success": False, "error": sv_result.get("error", "Unknown error")}

    probs = sv_result["probabilities"]
    state_desc = format_state_description(probs, qubits)

    return {
        "success": True,
        "step_index": step_index,
        "gate_applied": gate_applied,
        "state_description": state_desc,
        "state_vector": sv_result["state_vector"],
        "probabilities": probs,
        "explanation": GATE_EXPLANATIONS.get(gate_applied, f"{gate_applied} gate applied."),
    }
