"""Quantum Fourier Transform."""
import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def _qft_circuit(n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            angle = 2 * math.pi / (2 ** (k - j + 1))
            qc.cp(angle, k, j)
    # SWAP
    for j in range(n // 2):
        qc.swap(j, n - j - 1)
    return qc


def run_qft(n_qubits: int = 3, input_state: int = 0) -> dict:
    n = max(1, min(n_qubits, 6))
    input_state = input_state % (2 ** n)

    qc = QuantumCircuit(n, n)

    # Encode input state
    bits = format(input_state, f"0{n}b")
    for i, bit in enumerate(reversed(bits)):
        if bit == "1":
            qc.x(i)

    qc.barrier()
    qft = _qft_circuit(n)
    qc.compose(qft, inplace=True)
    qc.barrier()
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    counts = sim.run(qc, shots=2048).result().get_counts(0)
    total = sum(counts.values())
    probabilities = {k: round(v / total, 4) for k, v in counts.items()}

    return {
        "algorithm": "qft",
        "n_qubits": n,
        "input_state": input_state,
        "input_binary": bits,
        "counts": counts,
        "probabilities": probabilities,
        "classical_complexity": f"O(N log N) = O({2**n} × {n})",
        "quantum_complexity": f"O(n²) = O({n**2})",
        "success": True,
    }
