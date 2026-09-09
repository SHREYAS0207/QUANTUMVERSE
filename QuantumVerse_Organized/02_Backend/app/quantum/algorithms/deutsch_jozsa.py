"""Deutsch-Jozsa algorithm."""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def _apply_oracle(qc: QuantumCircuit, n: int, oracle_type: str):
    if oracle_type == "constant_zero":
        pass  # do nothing
    elif oracle_type == "constant_one":
        qc.x(n)  # flip output qubit
    else:  # balanced: XOR with first qubit
        for i in range(n):
            qc.cx(i, n)


def run_deutsch_jozsa(oracle_type: str = "balanced", n_qubits: int = 3) -> dict:
    n = max(1, min(n_qubits, 5))
    if oracle_type not in ("constant_zero", "constant_one", "balanced"):
        oracle_type = "balanced"

    qc = QuantumCircuit(n + 1, n)

    # Initialize: input qubits |0⟩, output qubit |1⟩
    qc.x(n)
    qc.h(range(n + 1))
    qc.barrier()

    # Oracle
    _apply_oracle(qc, n, oracle_type)
    qc.barrier()

    # Hadamard on input qubits
    qc.h(range(n))
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    counts = sim.run(qc, shots=1024).result().get_counts(0)
    total = sum(counts.values())

    # If all input qubits are 0, function is constant; otherwise balanced
    all_zero = "0" * n
    zero_prob = counts.get(all_zero, 0) / total
    result = "constant" if zero_prob > 0.9 else "balanced"
    is_correct = (
        (result == "constant" and oracle_type.startswith("constant")) or
        (result == "balanced" and oracle_type == "balanced")
    )

    return {
        "algorithm": "deutsch_jozsa",
        "oracle_type": oracle_type,
        "n_qubits": n,
        "result": result,
        "is_correct": is_correct,
        "counts": counts,
        "probabilities": {k: round(v / total, 4) for k, v in counts.items()},
        "all_zeros_probability": round(zero_prob, 4),
        "classical_queries_needed": f"2^({n}-1) + 1 = {2**(n-1)+1}",
        "quantum_queries_needed": "1",
        "success": True,
    }
