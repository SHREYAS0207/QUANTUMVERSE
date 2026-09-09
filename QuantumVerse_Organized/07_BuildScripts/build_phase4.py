import os

BASE = "/data/quantumverse"

files = {}

# ======================================================================
# BACKEND: Complete Quantum Engine
# ======================================================================

files["backend/app/quantum/engine.py"] = '''
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
'''

files["backend/app/quantum/simulator.py"] = '''
"""Qiskit Aer simulation engine."""
import time
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
    from qiskit_aer import StatevectorSimulator

    sv_sim = StatevectorSimulator()

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
        job = sv_sim.run(qc)
        sv = job.result().get_statevector(0)
        amps = [(float(a.real), float(a.imag)) for a in sv]
        probs = {format(i, f"0{qubits}b"): abs(a) ** 2 for i, a in enumerate(sv)}
        probs = {k: round(v, 6) for k, v in probs.items() if v > 1e-8}
        return {"success": True, "state_vector": amps, "probabilities": probs}
    except Exception as exc:
        return {"success": False, "error": str(exc), "state_vector": [], "probabilities": {}}
'''

files["backend/app/quantum/step_executor.py"] = '''
"""Step-by-step gate execution with explanations."""
from .simulator import run_statevector

GATE_EXPLANATIONS = {
    "H":    "Hadamard gate — puts qubit into equal superposition. |0\u27e9 \u2192 \u00bd(|0\u27e9+|1\u27e9), |1\u27e9 \u2192 \u00bd(|0\u27e9-|1\u27e9).",
    "X":    "Pauli-X (NOT) gate — flips qubit state: |0\u27e9 \u2192 |1\u27e9 and |1\u27e9 \u2192 |0\u27e9.",
    "Y":    "Pauli-Y gate — combines X and Z rotations with an imaginary phase factor.",
    "Z":    "Pauli-Z gate — phase flip: |0\u27e9 unchanged, |1\u27e9 \u2192 -|1\u27e9. No visible effect until interference.",
    "S":    "S gate (\u221aZ) — applies a 90\u00b0 phase rotation to |1\u27e9. Used in QFT.",
    "T":    "T gate (\u221aS) — applies a 45\u00b0 phase rotation. Important for universal quantum computing.",
    "SDG":  "S-dagger — inverse S gate, -90\u00b0 phase rotation.",
    "TDG":  "T-dagger — inverse T gate, -45\u00b0 phase rotation.",
    "RX":   "Rotation around X-axis by angle \u03b8. Generalization of the X gate.",
    "RY":   "Rotation around Y-axis. Used to create arbitrary superpositions.",
    "RZ":   "Rotation around Z-axis. Applies a relative phase without changing probabilities.",
    "CNOT": "Controlled-NOT — flips target qubit only when control is |1\u27e9. Creates entanglement!",
    "CX":   "Controlled-X (same as CNOT). The workhorse two-qubit gate.",
    "CZ":   "Controlled-Z — applies Z to target when control is |1\u27e9. Symmetric in effect.",
    "SWAP": "SWAP — exchanges two qubit states completely.",
    "CCX":  "Toffoli (CCX) — flips target when both controls are |1\u27e9. Reversible NAND.",
    "MEASURE": "Measurement — collapses superposition to |0\u27e9 or |1\u27e9 with Born-rule probabilities.",
    "BARRIER": "Barrier — visual/compilation separator. No physical effect.",
}


def format_state_description(probabilities: dict, qubits: int) -> str:
    """Return a human-readable state description."""
    dominant = [(s, p) for s, p in probabilities.items() if p > 0.001]
    dominant.sort(key=lambda x: -x[1])
    if not dominant:
        return "|0\u27e9" * qubits
    if len(dominant) == 1:
        return f"|{dominant[0][0]}\u27e9"
    parts = " + ".join(
        f"{round(p**0.5, 2)}|{s}\u27e9" for s, p in dominant[:4]
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
            "gate_applied": "INIT", "state_description": f"|{'0' * qubits}\u27e9",
            "state_vector": [(1.0, 0.0)] + [(0.0, 0.0)] * (2 ** qubits - 1),
            "probabilities": {"0" * qubits: 1.0},
            "explanation": f"Initial state: all {qubits} qubits in |0\u27e9.",
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
'''

# ======================================================================
# BACKEND: Complete Algorithm Implementations
# ======================================================================

files["backend/app/quantum/algorithms/grover.py"] = '''
"""Grover\'s search algorithm."""
import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def run_grover(n_qubits: int, target: int, iterations: int | None = None) -> dict:
    """Run Grover\'s algorithm to find `target` in a database of 2^n_qubits items."""
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
        "quantum_complexity": f"O(\u221a{N} \u2248 {round(math.sqrt(N), 1)})",
        "success": True,
    }
'''

files["backend/app/quantum/algorithms/teleportation.py"] = '''
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

    # Qubit 2 (rightmost bit in Qiskit\'s ordering) should match original
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
            {"step": 1, "description": f"Prepared qubit 0 in |{state}\u27e9 state"},
            {"step": 2, "description": "Created Bell pair |\u03a6+\u27e9 between qubits 1 and 2"},
            {"step": 3, "description": "Performed Bell measurement on sender qubits 0 and 1"},
            {"step": 4, "description": "Applied classical corrections on receiver (qubit 2)"},
            {"step": 5, "description": "Teleportation complete — qubit state transferred!"},
        ],
        "success": True,
    }
'''

files["backend/app/quantum/algorithms/deutsch_jozsa.py"] = '''
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

    # Initialize: input qubits |0\u27e9, output qubit |1\u27e9
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
'''

files["backend/app/quantum/algorithms/qft.py"] = '''
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
        "classical_complexity": f"O(N log N) = O({2**n} \u00d7 {n})",
        "quantum_complexity": f"O(n\u00b2) = O({n**2})",
        "success": True,
    }
'''

# ======================================================================
# BACKEND: Complete API Routes
# ======================================================================

files["backend/app/api/v1/auth.py"] = '''
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import create_access_token, verify_password, hash_password
from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=body.name,
        email=body.email,
        password_hash=hash_password(body.password),
        learning_level=body.learning_level,
    )
    db.add(user)
    await db.flush()

    profile = UserProfile(user_id=user.id)
    db.add(profile)
    await db.commit()
    await db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token, token_type="bearer",
        user_id=str(user.id), name=user.name, email=user.email,
        learning_level=user.learning_level,
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token, token_type="bearer",
        user_id=str(user.id), name=user.name, email=user.email,
        learning_level=user.learning_level,
    )


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed = {"name", "learning_level"}
    for key, val in body.items():
        if key in allowed:
            setattr(current_user, key, val)
    await db.commit()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)
'''

files["backend/app/api/v1/simulation.py"] = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.circuit import SimulationHistory
from app.quantum.simulator import run_simulation
from app.quantum.step_executor import execute_step
from pydantic import BaseModel
from typing import Any

router = APIRouter(prefix="/simulation", tags=["simulation"])


class RunRequest(BaseModel):
    qubits: int = 2
    classical_bits: int = 2
    operations: list[dict[str, Any]] = []
    shots: int = 1024
    circuit_id: str | None = None


class StepRequest(BaseModel):
    qubits: int = 2
    operations: list[dict[str, Any]] = []
    step_index: int = 0


@router.post("/run")
async def run(body: RunRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = run_simulation(body.qubits, body.classical_bits, body.operations, body.shots)

    # Persist to history
    hist = SimulationHistory(
        user_id=user.id,
        circuit_id=body.circuit_id,
        shots=body.shots,
        result_data=result,
    )
    db.add(hist)
    await db.commit()

    return result


@router.post("/step")
async def step(body: StepRequest, user: User = Depends(get_current_user)):
    return execute_step(body.qubits, body.operations, body.step_index)


@router.get("/history")
async def history(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    from sqlalchemy import select, desc
    rows = await db.execute(
        select(SimulationHistory).where(SimulationHistory.user_id == user.id).order_by(desc(SimulationHistory.created_at)).limit(20)
    )
    items = rows.scalars().all()
    return {"history": [{
        "id": str(h.id),
        "circuit_id": str(h.circuit_id) if h.circuit_id else None,
        "shots": h.shots,
        "created_at": h.created_at.isoformat(),
        "result": h.result_data,
    } for h in items]}
'''

files["backend/app/api/v1/algorithms.py"] = '''
from fastapi import APIRouter
from pydantic import BaseModel

from app.quantum.algorithms.grover import run_grover
from app.quantum.algorithms.teleportation import run_teleportation
from app.quantum.algorithms.deutsch_jozsa import run_deutsch_jozsa
from app.quantum.algorithms.qft import run_qft

router = APIRouter(prefix="/algorithms", tags=["algorithms"])

ALGORITHMS_META = [
    {"id": "grover",          "name": "Grover\'s Search",           "complexity": "O(\u221aN)",        "category": "search"},
    {"id": "teleportation",   "name": "Quantum Teleportation",      "complexity": "3 qubits",       "category": "communication"},
    {"id": "deutsch-jozsa",   "name": "Deutsch-Jozsa",             "complexity": "O(1) queries",   "category": "query"},
    {"id": "qft",             "name": "Quantum Fourier Transform",  "complexity": "O(n\u00b2)",        "category": "transform"},
]


@router.get("")
async def list_algorithms():
    return {"algorithms": ALGORITHMS_META}


class GroverRequest(BaseModel):
    n_qubits: int = 3
    target: int = 5
    iterations: int | None = None


class TeleportRequest(BaseModel):
    state: str = "plus"


class DeutschJozsaRequest(BaseModel):
    oracle_type: str = "balanced"
    n_qubits: int = 3


class QFTRequest(BaseModel):
    n_qubits: int = 3
    input_state: int = 0


@router.post("/grover/run")
async def grover(body: GroverRequest):
    return run_grover(body.n_qubits, body.target, body.iterations)


@router.post("/teleportation/run")
async def teleportation(body: TeleportRequest):
    return run_teleportation(body.state)


@router.post("/deutsch-jozsa/run")
async def deutsch_jozsa(body: DeutschJozsaRequest):
    return run_deutsch_jozsa(body.oracle_type, body.n_qubits)


@router.post("/qft/run")
async def qft(body: QFTRequest):
    return run_qft(body.n_qubits, body.input_state)
'''

files["backend/app/api/v1/circuits.py"] = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import Any
import uuid

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.circuit import Circuit

router = APIRouter(prefix="/circuits", tags=["circuits"])


class CircuitBody(BaseModel):
    name: str = "My Circuit"
    description: str | None = None
    qubits: int = 2
    classical_bits: int = 2
    circuit_data: dict[str, Any] = {}


@router.get("")
async def list_circuits(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(
        select(Circuit).where(Circuit.user_id == user.id, Circuit.is_template == False)
        .order_by(desc(Circuit.updated_at)).limit(50)
    )
    items = rows.scalars().all()
    return {"circuits": [_circuit_dict(c) for c in items]}


@router.post("", status_code=201)
async def create_circuit(body: CircuitBody, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = Circuit(
        user_id=user.id, name=body.name, description=body.description,
        qubits=body.qubits, classical_bits=body.classical_bits,
        circuit_data=body.circuit_data, is_template=False,
    )
    db.add(c)
    await db.commit()
    await db.refresh(c)

    # Update stats
    user.profile.total_circuits = (user.profile.total_circuits or 0) + 1
    await db.commit()

    return _circuit_dict(c)


@router.get("/templates")
async def list_templates(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(select(Circuit).where(Circuit.is_template == True))
    return {"templates": [_circuit_dict(c) for c in rows.scalars().all()]}


@router.get("/{circuit_id}")
async def get_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = await _get_or_404(db, circuit_id, user.id)
    return _circuit_dict(c)


@router.put("/{circuit_id}")
async def update_circuit(circuit_id: str, body: CircuitBody, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = await _get_or_404(db, circuit_id, user.id)
    c.name = body.name
    c.description = body.description
    c.qubits = body.qubits
    c.classical_bits = body.classical_bits
    c.circuit_data = body.circuit_data
    await db.commit()
    await db.refresh(c)
    return _circuit_dict(c)


@router.delete("/{circuit_id}", status_code=204)
async def delete_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = await _get_or_404(db, circuit_id, user.id)
    await db.delete(c)
    await db.commit()


async def _get_or_404(db: AsyncSession, circuit_id: str, user_id: uuid.UUID) -> Circuit:
    row = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.user_id == user_id))
    c = row.scalar_one_or_none()
    if not c:
        raise HTTPException(404, "Circuit not found")
    return c


def _circuit_dict(c: Circuit) -> dict:
    return {
        "id": str(c.id), "name": c.name, "description": c.description,
        "qubits": c.qubits, "classical_bits": c.classical_bits,
        "circuit_data": c.circuit_data, "is_template": c.is_template,
        "created_at": c.created_at.isoformat(), "updated_at": c.updated_at.isoformat(),
    }
'''

files["backend/app/api/v1/learning.py"] = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.learning import LearningModule, Lesson, LessonProgress

router = APIRouter(prefix="/learning", tags=["learning"])


@router.get("/modules")
async def list_modules(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(LearningModule).order_by(LearningModule.level, LearningModule.order_index))
    modules = rows.scalars().all()
    return {"modules": [{
        "id": str(m.id), "title": m.title, "description": m.description,
        "level": m.level, "icon": m.icon, "lesson_count": m.lesson_count,
    } for m in modules]}


@router.get("/modules/{module_id}")
async def get_module(module_id: str, db: AsyncSession = Depends(get_db)):
    row = await db.execute(select(LearningModule).where(LearningModule.id == module_id))
    module = row.scalar_one_or_none()
    if not module:
        raise HTTPException(404, "Module not found")
    rows = await db.execute(select(Lesson).where(Lesson.module_id == module_id).order_by(Lesson.order_index))
    lessons = rows.scalars().all()
    return {
        "id": str(module.id), "title": module.title, "description": module.description,
        "level": module.level, "lessons": [{
            "id": str(l.id), "title": l.title, "order_index": l.order_index,
            "xp_reward": l.xp_reward, "estimated_minutes": l.estimated_minutes,
        } for l in lessons],
    }


@router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: str, db: AsyncSession = Depends(get_db)):
    row = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = row.scalar_one_or_none()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return {
        "id": str(lesson.id), "title": lesson.title, "content": lesson.content,
        "xp_reward": lesson.xp_reward, "estimated_minutes": lesson.estimated_minutes,
    }


@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    lesson = (await db.execute(select(Lesson).where(Lesson.id == lesson_id))).scalar_one_or_none()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    existing = await db.execute(
        select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson_id)
    )
    if not existing.scalar_one_or_none():
        prog = LessonProgress(user_id=user.id, lesson_id=lesson_id, completed=True)
        db.add(prog)
        user.xp = (user.xp or 0) + lesson.xp_reward
        user.level = max(1, user.xp // 500 + 1)
        if user.profile:
            user.profile.total_lessons = (user.profile.total_lessons or 0) + 1
        await db.commit()

    return {"xp_earned": lesson.xp_reward, "total_xp": user.xp}


@router.get("/progress")
async def get_progress(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(
        select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.completed == True)
    )
    completed = [str(r.lesson_id) for r in rows.scalars().all()]
    return {"completed": completed, "in_progress": []}
'''

files["backend/app/api/v1/quiz.py"] = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.quiz import Quiz, Question, QuizAttempt

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/quizzes")
async def list_quizzes(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Quiz))
    quizzes = rows.scalars().all()
    return {"quizzes": [{
        "id": str(q.id), "title": q.title,
        "difficulty": q.difficulty, "xp_reward": q.xp_reward,
        "question_count": q.question_count,
    } for q in quizzes]}


@router.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id: str, db: AsyncSession = Depends(get_db)):
    row = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = row.scalar_one_or_none()
    if not quiz:
        raise HTTPException(404, "Quiz not found")
    rows = await db.execute(select(Question).where(Question.quiz_id == quiz_id).order_by(Question.order_index))
    questions = rows.scalars().all()
    return {
        "id": str(quiz.id), "title": quiz.title, "difficulty": quiz.difficulty,
        "xp_reward": quiz.xp_reward, "time_limit_seconds": quiz.time_limit_seconds,
        "questions": [{
            "id": str(q.id), "question_text": q.question_text,
            "question_type": q.question_type,
            "options": q.options or [],
            "correct_answer": q.correct_answer,  # include for client-side validation
        } for q in questions],
    }


class SubmitBody(BaseModel):
    answers: dict[str, str]
    time_taken: int = 0


@router.post("/quizzes/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: str, body: SubmitBody,
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    quiz = (await db.execute(select(Quiz).where(Quiz.id == quiz_id))).scalar_one_or_none()
    if not quiz:
        raise HTTPException(404, "Quiz not found")

    rows = await db.execute(select(Question).where(Question.quiz_id == quiz_id))
    questions = rows.scalars().all()

    correct = 0
    answer_results = []
    for q in questions:
        user_ans = body.answers.get(str(q.id), "")
        is_correct = user_ans == q.correct_answer
        if is_correct:
            correct += 1
        answer_results.append({
            "question_id": str(q.id),
            "user_answer": user_ans,
            "is_correct": is_correct,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation or "",
        })

    total = len(questions)
    accuracy = round(correct / total * 100) if total else 0
    xp_earned = round(quiz.xp_reward * accuracy / 100)

    attempt = QuizAttempt(
        user_id=user.id, quiz_id=quiz.id,
        score=correct, total_questions=total,
        time_taken=body.time_taken, xp_earned=xp_earned,
    )
    db.add(attempt)

    user.xp = (user.xp or 0) + xp_earned
    user.level = max(1, user.xp // 500 + 1)
    if user.profile:
        user.profile.total_quizzes = (user.profile.total_quizzes or 0) + 1
        prev_acc = user.profile.quiz_accuracy or 0
        count = user.profile.total_quizzes
        user.profile.quiz_accuracy = round((prev_acc * (count - 1) + accuracy) / count, 1)

    await db.commit()

    return {
        "score": correct, "total": total, "accuracy": accuracy,
        "xp_earned": xp_earned, "answers": answer_results,
    }
'''

files["backend/app/api/v1/achievements.py"] = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.achievement import Achievement, UserAchievement

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("")
async def list_achievements(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Achievement).order_by(Achievement.xp_reward))
    return {"achievements": [{
        "id": str(a.id), "name": a.name, "description": a.description,
        "badge_icon": a.badge_icon, "badge_color": a.badge_color, "xp_reward": a.xp_reward,
    } for a in rows.scalars().all()]}


@router.get("/user")
async def user_achievements(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(select(UserAchievement).where(UserAchievement.user_id == user.id))
    return {"unlocked": [{
        "achievement_id": str(ua.achievement_id),
        "unlocked_at": ua.unlocked_at.isoformat(),
    } for ua in rows.scalars().all()]}
'''

files["backend/app/api/v1/ai_tutor.py"] = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.ai import AIConversation, AIMessage
from app.ai.provider import get_ai_response

router = APIRouter(prefix="/ai", tags=["ai_tutor"])


@router.post("/conversations", status_code=201)
async def create_conversation(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    conv = AIConversation(user_id=user.id, title="New Conversation")
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return {"id": str(conv.id), "title": conv.title}


@router.get("/conversations")
async def list_conversations(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(
        select(AIConversation).where(AIConversation.user_id == user.id).order_by(desc(AIConversation.updated_at)).limit(20)
    )
    return {"conversations": [{"id": str(c.id), "title": c.title, "updated_at": c.updated_at.isoformat()} for c in rows.scalars().all()]}


class ChatBody(BaseModel):
    message: str
    difficulty: str = "beginner"
    context: dict[str, Any] | None = None


@router.post("/conversations/{conv_id}/chat")
async def chat(
    conv_id: str, body: ChatBody,
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    conv = (await db.execute(select(AIConversation).where(AIConversation.id == conv_id, AIConversation.user_id == user.id))).scalar_one_or_none()
    if not conv:
        raise HTTPException(404, "Conversation not found")

    # Get last 10 messages for context
    history_rows = await db.execute(
        select(AIMessage).where(AIMessage.conversation_id == conv_id).order_by(AIMessage.created_at).limit(10)
    )
    history = [{"role": m.role, "content": m.content} for m in history_rows.scalars().all()]

    # Save user message
    user_msg = AIMessage(conversation_id=conv_id, role="user", content=body.message)
    db.add(user_msg)

    # Get AI response
    ai_text = await get_ai_response(body.message, history, body.difficulty, body.context)

    # Save AI response
    ai_msg = AIMessage(conversation_id=conv_id, role="assistant", content=ai_text)
    db.add(ai_msg)

    # Update conversation title from first message
    if not history:
        conv.title = body.message[:60] + ("..." if len(body.message) > 60 else "")

    await db.commit()
    return {"response": ai_text, "conversation_id": conv_id}


class ExplainBody(BaseModel):
    circuit_data: dict[str, Any]
    difficulty: str = "beginner"


@router.post("/explain-circuit")
async def explain_circuit(body: ExplainBody, user: User = Depends(get_current_user)):
    ops = body.circuit_data.get("operations", [])
    gates = [op.get("gate") for op in ops]
    prompt = f"Explain this quantum circuit step by step for a {body.difficulty} student. Gates used: {', '.join(gates)}. Total gates: {len(ops)}."
    explanation = await get_ai_response(prompt, [], body.difficulty)
    return {"explanation": explanation, "gate_count": len(ops), "gates": list(set(gates))}
'''

files["backend/app/api/v1/router.py"] = '''
from fastapi import APIRouter
from .auth import router as auth_router
from .circuits import router as circuits_router
from .simulation import router as simulation_router
from .algorithms import router as algorithms_router
from .learning import router as learning_router
from .ai_tutor import router as ai_router
from .quiz import router as quiz_router
from .achievements import router as achievements_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(circuits_router)
api_router.include_router(simulation_router)
api_router.include_router(algorithms_router)
api_router.include_router(learning_router)
api_router.include_router(ai_router)
api_router.include_router(quiz_router)
api_router.include_router(achievements_router)
'''

# ======================================================================
# BACKEND: AI Provider
# ======================================================================

files["backend/app/ai/provider.py"] = '''
"""LLM abstraction layer using OpenRouter."""
import httpx
from app.core.config import settings


SYSTEM_PROMPTS = {
    "beginner": """You are QubitAI, an expert quantum computing tutor for beginners.
Explain concepts using simple analogies (coins, light switches, balls in boxes).
Avoid heavy math. Focus on intuition. Keep answers concise (3-5 sentences max unless asked for more).
If asked about quantum gates, use visual analogies.""",

    "intermediate": """You are QubitAI, a quantum computing tutor for intermediate learners.
You can use linear algebra, Dirac notation (|0⟩, |1⟩), and Bloch sphere descriptions.
Explain the math but keep it accessible. Connect theory to real circuit implementations.""",

    "advanced": """You are QubitAI, an expert quantum computing mentor for advanced students.
Use full mathematical formalism: density matrices, tensor products, unitary operators, Hamiltonians.
Discuss quantum complexity theory, error correction, and NISQ-era limitations when relevant.""",
}

FALLBACK_RESPONSES = {
    "beginner": "Quantum computing uses the weird rules of quantum physics — like superposition (being in two states at once) and entanglement (spooky action at a distance) — to perform certain calculations exponentially faster than classical computers.",
    "intermediate": "Quantum computing leverages quantum mechanical phenomena — superposition, entanglement, and interference — to encode and process information in qubits, enabling polynomial or exponential speedups for specific problem classes.",
    "advanced": "Quantum computing exploits the exponentially large Hilbert space of n-qubit systems and quantum mechanical operations (unitary evolution, projective measurement) to solve certain computational problems in BQP that are believed classically intractable.",
}


async def get_ai_response(
    message: str,
    history: list[dict],
    difficulty: str = "beginner",
    context: dict | None = None,
) -> str:
    if not settings.OPENROUTER_API_KEY or settings.OPENROUTER_API_KEY == "your-openrouter-key-here":
        return _fallback_response(message, difficulty)

    system = SYSTEM_PROMPTS.get(difficulty, SYSTEM_PROMPTS["beginner"])
    if context:
        system += f"\n\nCurrent context: {context}"

    messages = [{"role": "system", "content": system}]
    messages.extend(history[-8:])  # last 8 messages for context
    messages.append({"role": "user", "content": message})

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://quantumverse.ai",
                    "X-Title": "QuantumVerse AI",
                },
                json={
                    "model": settings.AI_MODEL,
                    "messages": messages,
                    "max_tokens": 800,
                    "temperature": 0.7,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        return _fallback_response(message, difficulty)


def _fallback_response(message: str, difficulty: str) -> str:
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["superposition", "what is quantum"]):
        return FALLBACK_RESPONSES.get(difficulty, FALLBACK_RESPONSES["beginner"])
    if any(w in msg_lower for w in ["hadamard", " h gate"]):
        return "The Hadamard gate creates equal superposition: it maps |0\u27e9 \u2192 \u00bd(|0\u27e9+|1\u27e9) and |1\u27e9 \u2192 \u00bd(|0\u27e9-|1\u27e9). Think of it as a quantum coin flip that leaves the coin spinning."
    if "entangle" in msg_lower:
        return "Quantum entanglement links two qubits so that measuring one instantly determines the state of the other, no matter how far apart they are. It\'s created by combining a Hadamard gate with a CNOT gate."
    if "grover" in msg_lower:
        return "Grover\'s algorithm searches an unsorted database of N items in O(\u221aN) steps, compared to O(N) classically — a quadratic speedup. It works by amplifying the amplitude of the target state through repeated oracle + diffusion steps."
    return "That\'s a great quantum computing question! To get full AI-powered answers, add your OpenRouter API key to the backend .env file. I can explain any quantum concept, gate, or algorithm in depth."
'''

# ======================================================================
# BACKEND: Config + Main App updates
# ======================================================================

files["backend/app/core/config.py"] = '''
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "QuantumVerse AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/quantumverse"

    SECRET_KEY: str = "change-me-in-production-use-256-bit-random-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    OPENROUTER_API_KEY: str = "your-openrouter-key-here"
    AI_MODEL: str = "meta-llama/llama-3.1-8b-instruct:free"

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://quantumverse.vercel.app",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
'''

files["backend/app/core/security.py"] = '''
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return _pwd.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload["exp"] = expire
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
'''

files["backend/app/core/dependencies.py"] = '''
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import decode_token
from app.database.session import get_db
from app.models.user import User

_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
'''

files["backend/app/main.py"] = '''
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.connection import engine
from app.models.user import Base as UserBase
from app.models.circuit import Base as CircuitBase
from app.models.learning import Base as LearningBase
from app.models.quiz import Base as QuizBase
from app.models.achievement import Base as AchievementBase
from app.models.ai import Base as AIBase
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        for base in [UserBase, CircuitBase, LearningBase, QuizBase, AchievementBase, AIBase]:
            await conn.run_sync(base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Quantum Algorithm Learning and Simulation Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": settings.APP_VERSION, "app": settings.APP_NAME}
'''

# ======================================================================
# BACKEND: Complete Schemas
# ======================================================================

files["backend/app/schemas/auth.py"] = '''
from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    learning_level: Literal["beginner", "intermediate", "advanced"] = "beginner"

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("name")
    @classmethod
    def check_name(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    email: str
    learning_level: str


class UserStatistics(BaseModel):
    total_lessons: int = 0
    total_circuits: int = 0
    total_quizzes: int = 0
    quiz_accuracy: float = 0.0

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    learning_level: str
    xp: int
    level: int
    streak_days: int
    statistics: UserStatistics

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        profile = getattr(obj, "profile", None)
        stats = UserStatistics(
            total_lessons=getattr(profile, "total_lessons", 0) or 0,
            total_circuits=getattr(profile, "total_circuits", 0) or 0,
            total_quizzes=getattr(profile, "total_quizzes", 0) or 0,
            quiz_accuracy=getattr(profile, "quiz_accuracy", 0.0) or 0.0,
        ) if profile else UserStatistics()
        return cls(
            id=str(obj.id), name=obj.name, email=obj.email,
            learning_level=obj.learning_level or "beginner",
            xp=obj.xp or 0, level=obj.level or 1, streak_days=obj.streak_days or 0,
            statistics=stats,
        )
'''

# ======================================================================
# BACKEND: Test Suite
# ======================================================================

files["backend/tests/test_quantum.py"] = '''
"""Tests for the Qiskit quantum engine."""
import pytest
from app.quantum.simulator import run_simulation
from app.quantum.step_executor import execute_step
from app.quantum.algorithms.grover import run_grover
from app.quantum.algorithms.deutsch_jozsa import run_deutsch_jozsa
from app.quantum.algorithms.qft import run_qft
from app.quantum.algorithms.teleportation import run_teleportation


def test_single_qubit_x_gate():
    ops = [{"gate": "X", "targets": [0], "controls": [], "column": 0}]
    result = run_simulation(1, 1, ops, shots=512)
    assert result["success"]
    assert result["counts"].get("1", 0) > 490, "X gate should flip |0> to |1>"


def test_hadamard_superposition():
    ops = [{"gate": "H", "targets": [0], "controls": [], "column": 0}]
    result = run_simulation(1, 1, ops, shots=1000)
    assert result["success"]
    counts = result["counts"]
    assert abs(counts.get("0", 0) - counts.get("1", 0)) < 150, "H gate should give ~50/50"


def test_bell_state():
    ops = [
        {"gate": "H",    "targets": [0], "controls": [],  "column": 0},
        {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1},
    ]
    result = run_simulation(2, 2, ops, shots=1000)
    assert result["success"]
    counts = result["counts"]
    # Bell state |00> + |11> - only 00 and 11 should appear
    assert counts.get("01", 0) < 50
    assert counts.get("10", 0) < 50


def test_step_executor():
    ops = [
        {"gate": "H", "targets": [0], "controls": [], "column": 0},
        {"gate": "X", "targets": [1], "controls": [], "column": 1},
    ]
    result = execute_step(2, ops, 0)
    assert result["success"]
    assert result["gate_applied"] == "H"
    assert "probabilities" in result


def test_grover():
    result = run_grover(3, 5)
    assert result["success"]
    assert result["target_probability"] > 0.5, "Grover should have high probability for target"


def test_deutsch_jozsa_constant():
    result = run_deutsch_jozsa("constant_zero", 3)
    assert result["success"]
    assert result["result"] == "constant"


def test_deutsch_jozsa_balanced():
    result = run_deutsch_jozsa("balanced", 3)
    assert result["success"]
    assert result["result"] == "balanced"


def test_qft():
    result = run_qft(3, 0)
    assert result["success"]
    assert "probabilities" in result


def test_teleportation():
    result = run_teleportation("plus")
    assert result["success"]
    assert "steps" in result
    assert len(result["steps"]) == 5
'''

files["backend/tests/test_api.py"] = '''
"""Integration tests for QuantumVerse API."""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.anyio
async def test_signup_and_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Signup
        res = await client.post("/api/v1/auth/signup", json={
            "name": "Test User", "email": "test@quantumverse.ai",
            "password": "testpass123", "learning_level": "beginner",
        })
        assert res.status_code == 201
        token = res.json()["access_token"]

        # Profile
        profile = await client.get("/api/v1/auth/profile", headers={"Authorization": f"Bearer {token}"})
        assert profile.status_code == 200
        assert profile.json()["name"] == "Test User"


@pytest.mark.anyio
async def test_algorithms_list():
    async with AsyncClient(app=app, base_url="http://test") as client:
        res = await client.get("/api/v1/algorithms")
    assert res.status_code == 200
    assert len(res.json()["algorithms"]) == 4
'''

# ======================================================================
# FRONTEND: Phase 4 additions
# ======================================================================

FRONTEND_BASE = "/data/quantumverse/frontend"

front_files = {}

front_files["src/components/shared/XPToast.tsx"] = '''
"use client";
import { motion, AnimatePresence } from "framer-motion";
import { Zap } from "lucide-react";

interface XPToastProps {
  xp: number;
  visible: boolean;
}

export function XPToast({ xp, visible }: XPToastProps) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.8 }}
          className="fixed bottom-8 right-8 z-50 flex items-center gap-2 px-5 py-3 rounded-2xl bg-quantum-blue text-quantum-dark font-bold shadow-[0_0_30px_rgba(0,212,255,0.4)]"
        >
          <Zap className="w-5 h-5" />
          <span>+{xp} XP</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
'''

front_files["src/components/shared/GlowButton.tsx"] = '''
"use client";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface GlowButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  loading?: boolean;
  children: React.ReactNode;
}

export function GlowButton({ variant = "primary", loading, children, className, ...props }: GlowButtonProps) {
  const base = "flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm transition-all disabled:opacity-60";
  const variants = {
    primary:   "bg-quantum-blue text-quantum-dark hover:opacity-90 shadow-[0_0_20px_rgba(0,212,255,0.3)] hover:shadow-[0_0_30px_rgba(0,212,255,0.5)]",
    secondary: "border border-quantum-blue/30 text-quantum-blue hover:bg-quantum-blue/10",
    danger:    "bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20",
    ghost:     "text-muted-foreground hover:text-white hover:bg-white/5",
  };

  return (
    <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
      className={cn(base, variants[variant], className)} disabled={loading} {...(props as any)}>
      {loading && <div className="w-4 h-4 border-2 border-current/30 border-t-current rounded-full animate-spin" />}
      {children}
    </motion.button>
  );
}
'''

front_files["src/components/shared/QuantumBadge.tsx"] = '''
import { cn } from "@/lib/utils";

type BadgeVariant = "blue" | "purple" | "cyan" | "green" | "yellow" | "red" | "gray";

const COLORS: Record<BadgeVariant, string> = {
  blue:   "text-blue-400   border-blue-400/30   bg-blue-400/5",
  purple: "text-purple-400 border-purple-400/30 bg-purple-400/5",
  cyan:   "text-cyan-400   border-cyan-400/30   bg-cyan-400/5",
  green:  "text-green-400  border-green-400/30  bg-green-400/5",
  yellow: "text-yellow-400 border-yellow-400/30 bg-yellow-400/5",
  red:    "text-red-400    border-red-400/30    bg-red-400/5",
  gray:   "text-gray-400   border-gray-400/30   bg-gray-400/5",
};

interface QuantumBadgeProps {
  label: string;
  variant?: BadgeVariant;
  className?: string;
}

export function QuantumBadge({ label, variant = "blue", className }: QuantumBadgeProps) {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${COLORS[variant]} ${className ?? ""}`}>
      {label}
    </span>
  );
}
'''

front_files["src/components/shared/EmptyState.tsx"] = '''
import type { LucideIcon } from "lucide-react";

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export function EmptyState({ icon: Icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="glass rounded-xl border border-white/5 flex flex-col items-center justify-center py-16 px-8 text-center">
      <Icon className="w-12 h-12 text-muted-foreground/20 mb-4" />
      <p className="text-white font-medium mb-1">{title}</p>
      {description && <p className="text-xs text-muted-foreground">{description}</p>}
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}
'''

# Write backend files
for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content.lstrip('\n'))
    print(f"  BE: {rel_path}")

# Write frontend files
for rel_path, content in front_files.items():
    full_path = os.path.join(FRONTEND_BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content.lstrip('\n'))
    print(f"  FE: {rel_path}")

print(f"\nPhase 4 files: {len(files)} backend + {len(front_files)} frontend = {len(files)+len(front_files)} total")
