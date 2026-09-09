"""Grover's search algorithm."""
import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def run_grover(n_qubits: int, target: int, iterations: int | None = None) -> dict:
    """Run Grover's algorithm to find `target` in a database of 2^n_qubits items."""
    n = max(2, min(n_qubits, 5))
    N = 2 ** n
    target = target % N

    if iterations is None:
        iterations = max(1, round(math.pi / 4 * math.sqrt(N)))

    qc = QuantumCircuit(n, n)

    # Initialise: equal superposition
    qc.h(range(n))

    for _ in range(iterations):
        # Oracle: mark the target state with a phase flip
        target_bits = format(target, f"0{n}b")
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)

        # Diffusion operator
        qc.h(range(n))
        qc.x(range(n))
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
        qc.x(range(n))
        qc.h(range(n))

    qc.measure(range(n), range(n))

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts(0)
    total = sum(counts.values())
    probabilities = {s: c / total for s, c in counts.items()}

    target_key = format(target, f"0{n}b")
    target_prob = probabilities.get(target_key, 0.0)

    return {
        "algorithm": "grover",
        "n_qubits": n,
        "search_space": N,
        "target": target_key,
        "iterations_used": iterations,
        "target_probability": round(target_prob, 4),
        "counts": counts,
        "probabilities": {k: round(v, 4) for k, v in probabilities.items()},
        "classical_complexity": f"O({N})",
        "quantum_complexity": f"O(√{N} ≈ {round(math.sqrt(N), 1)})",
        "success": True,
    }
