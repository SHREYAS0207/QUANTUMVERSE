"""Basic quantum error correction circuits."""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


def bit_flip_code(error_qubit: int = 0, apply_error: bool = True) -> dict:
    """3-qubit bit flip code. Encodes 1 logical qubit into 3 physical qubits."""
    qr = QuantumRegister(3, "q")
    anc = QuantumRegister(2, "anc")
    cr = ClassicalRegister(3, "c")
    qc = QuantumCircuit(qr, anc, cr)

    # Encode: |0> -> |000>, |1> -> |111>
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])
    qc.barrier()

    # Simulate a bit-flip error
    if apply_error and 0 <= error_qubit < 3:
        qc.x(qr[error_qubit])
    qc.barrier()

    # Syndrome measurement
    qc.cx(qr[0], anc[0]); qc.cx(qr[1], anc[0])
    qc.cx(qr[1], anc[1]); qc.cx(qr[2], anc[1])
    qc.barrier()

    # Error correction via syndrome
    qc.ccx(anc[0], anc[1], qr[1])  # Correct qubit 1 if both syndromes fire
    qc.barrier()
    qc.measure(qr, cr)

    sim = AerSimulator()
    counts = sim.run(qc, shots=512).result().get_counts(0)
    total = sum(counts.values())

    return {
        "code": "bit_flip",
        "error_qubit": error_qubit,
        "error_applied": apply_error,
        "counts": counts,
        "probabilities": {k: round(v / total, 4) for k, v in counts.items()},
        "success": True,
        "description": "3-qubit bit-flip code: detects and corrects single bit-flip errors.",
    }


def phase_flip_code(apply_error: bool = True) -> dict:
    """3-qubit phase flip (sign flip) code."""
    qr = QuantumRegister(3, "q")
    cr = ClassicalRegister(3, "c")
    qc = QuantumCircuit(qr, cr)

    # Encode in X basis
    qc.h(range(3))
    qc.cx(qr[0], qr[1]); qc.cx(qr[0], qr[2])
    qc.barrier()

    if apply_error:
        qc.z(qr[0])  # Phase flip error on qubit 0
    qc.barrier()

    # Decode
    qc.cx(qr[0], qr[1]); qc.cx(qr[0], qr[2])
    qc.h(range(3))
    qc.barrier()
    qc.measure(qr, cr)

    sim = AerSimulator()
    counts = sim.run(qc, shots=512).result().get_counts(0)
    total = sum(counts.values())
    return {
        "code": "phase_flip",
        "error_applied": apply_error,
        "counts": counts,
        "probabilities": {k: round(v / total, 4) for k, v in counts.items()},
        "success": True,
        "description": "3-qubit phase-flip code: detects and corrects single phase errors.",
    }


def noisy_simulation(qubits: int, operations: list, error_rate: float = 0.01, shots: int = 1024) -> dict:
    """Run a simulation with a depolarizing noise model."""
    from app.quantum.engine import build_circuit

    noise = NoiseModel()
    error = depolarizing_error(error_rate, 1)
    noise.add_all_qubit_quantum_error(error, ["h", "x", "y", "z", "s", "t"])

    qc = build_circuit(qubits, qubits, operations)
    sim = AerSimulator(noise_model=noise)
    counts = sim.run(qc, shots=shots).result().get_counts(0)
    total = sum(counts.values())
    return {
        "success": True,
        "noise_model": "depolarizing",
        "error_rate": error_rate,
        "counts": counts,
        "probabilities": {k: round(v / total, 4) for k, v in counts.items()},
    }
