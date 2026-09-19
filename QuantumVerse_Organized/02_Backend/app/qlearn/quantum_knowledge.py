"""
Quantum Knowledge Base — verified facts, concepts, equations, algorithms.
Used for RAG-style context injection into every AI call.
"""
from __future__ import annotations
import re
from typing import Optional

# ─────────────────────────────────────────────
# KNOWLEDGE ENTRIES
# Each entry: topic, category, difficulty, keywords, body
# ─────────────────────────────────────────────

KNOWLEDGE_BASE: list[dict] = [

# ── FOUNDATIONS ──────────────────────────────
{
"topic": "qubit",
"category": "FOUNDATION",
"difficulty": "beginner",
"keywords": ["qubit", "quantum bit", "two-level", "basis state", "|0>", "|1>"],
"body": (
    "A qubit is the fundamental unit of quantum information. Unlike a classical bit (0 or 1), "
    "a qubit exists in a superposition: |ψ⟩ = α|0⟩ + β|1⟩, where α,β ∈ ℂ and |α|²+|β|²=1. "
    "Measurement collapses the state: probability of |0⟩ is |α|², probability of |1⟩ is |β|². "
    "Physical implementations: superconducting circuits, trapped ions, photons, spin qubits."
),
},
{
"topic": "superposition",
"category": "FOUNDATION",
"difficulty": "beginner",
"keywords": ["superposition", "linear combination", "amplitude", "collapse"],
"body": (
    "Quantum superposition: a qubit can be in a linear combination of |0⟩ and |1⟩ simultaneously. "
    "|ψ⟩ = α|0⟩ + β|1⟩. The Hadamard gate creates equal superposition from |0⟩: "
    "H|0⟩ = (|0⟩+|1⟩)/√2, giving 50% probability for each outcome. "
    "Superposition is not classical probability — interference between amplitudes is possible."
),
},
{
"topic": "entanglement",
"category": "FOUNDATION",
"difficulty": "intermediate",
"keywords": ["entanglement", "bell state", "EPR", "non-local", "correlated", "spooky"],
"body": (
    "Quantum entanglement: two qubits whose states cannot be written as a product state. "
    "Bell state |Φ+⟩ = (|00⟩+|11⟩)/√2 is maximally entangled. "
    "Created by: H on qubit 0, then CNOT(control=0, target=1). "
    "Measuring qubit 0 instantly determines qubit 1 regardless of distance. "
    "Four Bell states: |Φ+⟩=(|00⟩+|11⟩)/√2, |Φ-⟩=(|00⟩-|11⟩)/√2, "
    "|Ψ+⟩=(|01⟩+|10⟩)/√2, |Ψ-⟩=(|01⟩-|10⟩)/√2."
),
},
{
"topic": "measurement",
"category": "FOUNDATION",
"difficulty": "beginner",
"keywords": ["measurement", "collapse", "born rule", "probability", "observable"],
"body": (
    "Quantum measurement (Born rule): measuring |ψ⟩=α|0⟩+β|1⟩ in the computational basis "
    "yields 0 with probability |α|² and 1 with probability |β|². "
    "After measurement the state collapses irreversibly. "
    "Measurement is non-unitary and destroys superposition. "
    "Expectation value of observable O: ⟨O⟩ = ⟨ψ|O|ψ⟩."
),
},
{
"topic": "bloch sphere",
"category": "FOUNDATION",
"difficulty": "intermediate",
"keywords": ["bloch sphere", "bloch vector", "polar", "azimuthal", "pure state"],
"body": (
    "Bloch sphere: geometric representation of a single qubit pure state. "
    "|ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩, where θ∈[0,π], φ∈[0,2π). "
    "North pole = |0⟩, South pole = |1⟩, equator = equal superpositions. "
    "|+⟩=(|0⟩+|1⟩)/√2 at (θ=π/2,φ=0), |-⟩=(|0⟩-|1⟩)/√2 at (θ=π/2,φ=π). "
    "Mixed states lie inside the sphere. Unitary gates are rotations on the sphere."
),
},

# ── MATHEMATICS ──────────────────────────────
{
"topic": "dirac notation",
"category": "MATHEMATICS",
"difficulty": "intermediate",
"keywords": ["bra", "ket", "dirac", "inner product", "outer product", "braket"],
"body": (
    "Dirac notation: |ψ⟩ is a ket (column vector), ⟨ψ| is a bra (row vector, conjugate transpose). "
    "Inner product: ⟨φ|ψ⟩ ∈ ℂ. Outer product: |ψ⟩⟨φ| is a matrix (operator). "
    "Orthonormality: ⟨0|0⟩=1, ⟨1|1⟩=1, ⟨0|1⟩=0. "
    "Completeness: |0⟩⟨0| + |1⟩⟨1| = I. "
    "Expectation value: ⟨A⟩ = ⟨ψ|A|ψ⟩."
),
},
{
"topic": "tensor product",
"category": "MATHEMATICS",
"difficulty": "intermediate",
"keywords": ["tensor product", "kronecker", "multi-qubit", "composite system", "⊗"],
"body": (
    "Tensor product (⊗) combines quantum systems. "
    "Two-qubit basis: |00⟩=|0⟩⊗|0⟩, |01⟩=|0⟩⊗|1⟩, |10⟩=|1⟩⊗|0⟩, |11⟩=|1⟩⊗|1⟩. "
    "n qubits → 2^n dimensional Hilbert space. "
    "H⊗H = (1/2)[[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]. "
    "Product state: |ψ⟩⊗|φ⟩ is separable. Entangled states cannot be written as a product."
),
},
{
"topic": "unitary operators",
"category": "MATHEMATICS",
"difficulty": "intermediate",
"keywords": ["unitary", "U†U", "reversible", "norm preserving", "quantum gate"],
"body": (
    "Quantum gates are unitary operators: U†U = UU† = I. "
    "Unitary operators preserve the norm of quantum states (probability conservation). "
    "All quantum gates are reversible: U^(-1) = U†. "
    "Single-qubit unitaries are 2×2 complex matrices with det = e^(iφ). "
    "Two-qubit unitaries are 4×4 matrices. n-qubit gates are 2^n × 2^n matrices."
),
},
{
"topic": "density matrix",
"category": "MATHEMATICS",
"difficulty": "advanced",
"keywords": ["density matrix", "mixed state", "trace", "partial trace", "von neumann"],
"body": (
    "Density matrix ρ = Σ_i p_i |ψ_i⟩⟨ψ_i|. Pure state: ρ=|ψ⟩⟨ψ|, Tr(ρ²)=1. "
    "Mixed state: Tr(ρ²)<1. Tr(ρ)=1 always. ρ is Hermitian and positive semidefinite. "
    "Evolution: ρ → UρU†. Measurement: p(m) = Tr(M_m ρ M_m†). "
    "Partial trace: ρ_A = Tr_B(ρ_AB) gives reduced state of subsystem A. "
    "Von Neumann entropy: S(ρ) = -Tr(ρ log ρ)."
),
},

# ── GATES ─────────────────────────────────────
{
"topic": "hadamard gate",
"category": "QUANTUM_GATE",
"difficulty": "beginner",
"keywords": ["hadamard", "H gate", "superposition", "H|0>", "H|1>"],
"body": (
    "Hadamard gate H = (1/√2)[[1,1],[1,-1]]. "
    "H|0⟩ = (|0⟩+|1⟩)/√2 = |+⟩. H|1⟩ = (|0⟩-|1⟩)/√2 = |-⟩. "
    "H² = I (self-inverse). Creates equal superposition. "
    "Bloch sphere: 180° rotation about the X+Z axis. "
    "H⊗n applied to |0⟩^n creates uniform superposition of all 2^n basis states."
),
},
{
"topic": "pauli gates",
"category": "QUANTUM_GATE",
"difficulty": "beginner",
"keywords": ["pauli", "X gate", "Y gate", "Z gate", "NOT gate", "bit flip", "phase flip"],
"body": (
    "Pauli-X (NOT): X=[[0,1],[1,0]]. X|0⟩=|1⟩, X|1⟩=|0⟩. Bit flip. "
    "Pauli-Y: Y=[[0,-i],[i,0]]. Y|0⟩=i|1⟩, Y|1⟩=-i|0⟩. Bit+phase flip. "
    "Pauli-Z: Z=[[1,0],[0,-1]]. Z|0⟩=|0⟩, Z|1⟩=-|1⟩. Phase flip. "
    "All Pauli gates are Hermitian and unitary. X²=Y²=Z²=I. "
    "Anticommutation: XY=-YX=iZ, YZ=-ZY=iX, ZX=-XZ=iY."
),
},
{
"topic": "CNOT gate",
"category": "QUANTUM_GATE",
"difficulty": "intermediate",
"keywords": ["CNOT", "controlled NOT", "CX", "entangling gate", "two qubit"],
"body": (
    "CNOT (Controlled-NOT): flips target qubit iff control qubit is |1⟩. "
    "Matrix (control=q0, target=q1): [[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]. "
    "CNOT|00⟩=|00⟩, CNOT|01⟩=|01⟩, CNOT|10⟩=|11⟩, CNOT|11⟩=|10⟩. "
    "H then CNOT creates Bell state from |00⟩. "
    "CNOT is its own inverse. Universal for quantum computing with single-qubit gates."
),
},
{
"topic": "phase gates",
"category": "QUANTUM_GATE",
"difficulty": "intermediate",
"keywords": ["S gate", "T gate", "phase", "Rz", "rotation", "T†", "Sdg"],
"body": (
    "S gate (phase): S=[[1,0],[0,i]]. S=√Z. S|0⟩=|0⟩, S|1⟩=i|1⟩. "
    "T gate: T=[[1,0],[0,e^(iπ/4)]]. T=√S. T|1⟩=e^(iπ/4)|1⟩. "
    "T† (T-dagger): T†=[[1,0],[0,e^(-iπ/4)]]. "
    "Rz(θ)=[[e^(-iθ/2),0],[0,e^(iθ/2)]]. Z=Rz(π), S=Rz(π/2), T=Rz(π/4). "
    "T gate is essential for universal quantum computation (with H and CNOT)."
),
},
{
"topic": "rotation gates",
"category": "QUANTUM_GATE",
"difficulty": "intermediate",
"keywords": ["Rx", "Ry", "Rz", "rotation", "parametric", "variational"],
"body": (
    "Rx(θ) = [[cos(θ/2), -i·sin(θ/2)], [-i·sin(θ/2), cos(θ/2)]]. "
    "Ry(θ) = [[cos(θ/2), -sin(θ/2)], [sin(θ/2), cos(θ/2)]]. "
    "Rz(θ) = [[e^(-iθ/2), 0], [0, e^(iθ/2)]]. "
    "Rx(π)=iX, Ry(π)=iY, Rz(π)=iZ. "
    "Any single-qubit unitary: U=e^(iα)Rz(β)Ry(γ)Rz(δ). Used in VQE/QAOA."
),
},
{
"topic": "toffoli gate",
"category": "QUANTUM_GATE",
"difficulty": "advanced",
"keywords": ["toffoli", "CCX", "CCNOT", "three qubit", "universal classical"],
"body": (
    "Toffoli (CCX): flips target qubit iff both control qubits are |1⟩. "
    "3-qubit gate, 8×8 unitary matrix. "
    "CCX|110⟩=|111⟩, CCX|111⟩=|110⟩, all others unchanged. "
    "Universal for classical reversible computation. "
    "Can implement AND gate: CCX|a,b,0⟩=|a,b,a AND b⟩. "
    "Decomposable into 6 CNOT gates + single-qubit gates."
),
},

# ── ALGORITHMS ────────────────────────────────
{
"topic": "deutsch jozsa algorithm",
"category": "QUANTUM_ALGORITHM",
"difficulty": "intermediate",
"keywords": ["deutsch", "deutsch-jozsa", "constant", "balanced", "oracle", "exponential"],
"body": (
    "Deutsch-Jozsa: determines if f:{0,1}^n→{0,1} is constant or balanced in 1 query. "
    "Classical: needs 2^(n-1)+1 queries worst case. Quantum: 1 query. "
    "Steps: (1) prepare |0⟩^n|1⟩, (2) apply H^⊗(n+1), (3) apply oracle U_f, "
    "(4) apply H^⊗n to first n qubits, (5) measure first n qubits. "
    "Result: all zeros → constant. Any nonzero → balanced. "
    "First algorithm showing exponential quantum speedup (for a specific problem)."
),
},
{
"topic": "grover algorithm",
"category": "QUANTUM_ALGORITHM",
"difficulty": "intermediate",
"keywords": ["grover", "search", "amplitude amplification", "oracle", "diffusion", "sqrt N"],
"body": (
    "Grover's algorithm: searches unsorted database of N items in O(√N) queries. "
    "Classical: O(N). Quantum speedup: quadratic. "
    "Steps: (1) H^⊗n creates uniform superposition, "
    "(2) Oracle flips phase of target: |x*⟩ → -|x*⟩, "
    "(3) Diffusion operator: D = 2|+⟩⟨+| - I (inversion about mean), "
    "(4) Repeat oracle+diffusion ≈ π√N/4 times, "
    "(5) Measure to find target with high probability. "
    "Optimal: cannot do better than O(√N) for unstructured search."
),
},
{
"topic": "shor algorithm",
"category": "QUANTUM_ALGORITHM",
"difficulty": "advanced",
"keywords": ["shor", "factoring", "period finding", "RSA", "QFT", "modular exponentiation"],
"body": (
    "Shor's algorithm: factors N-bit integer in O((log N)³) time. "
    "Classical best: sub-exponential but superpolynomial. Threatens RSA encryption. "
    "Key subroutine: quantum period finding using QFT. "
    "Steps: (1) choose random a < N, (2) find period r of f(x)=a^x mod N using QPE+QFT, "
    "(3) if r even and a^(r/2)≢-1 mod N, then gcd(a^(r/2)±1, N) gives factors. "
    "Requires: modular exponentiation circuit + QFT. "
    "Practical threat to 2048-bit RSA requires ~4000 logical qubits."
),
},
{
"topic": "quantum fourier transform",
"category": "QUANTUM_ALGORITHM",
"difficulty": "advanced",
"keywords": ["QFT", "quantum fourier transform", "DFT", "phase estimation", "frequency"],
"body": (
    "QFT: quantum analogue of DFT. Maps |j⟩ → (1/√N) Σ_k e^(2πijk/N)|k⟩. "
    "Classical DFT: O(N log N). QFT: O((log N)²) — exponential speedup. "
    "Circuit: n qubits, uses Hadamard + controlled-Rk gates. "
    "Rk = [[1,0],[0,e^(2πi/2^k)]]. "
    "Used in: Shor's algorithm, QPE, HHL, quantum simulation. "
    "QFT is not directly useful for speedup alone — must be combined with other subroutines."
),
},
{
"topic": "quantum phase estimation",
"category": "QUANTUM_ALGORITHM",
"difficulty": "advanced",
"keywords": ["QPE", "phase estimation", "eigenvalue", "eigenphase", "unitary"],
"body": (
    "QPE: estimates eigenphase φ of unitary U where U|ψ⟩=e^(2πiφ)|ψ⟩. "
    "Uses t ancilla qubits for t-bit precision. "
    "Steps: (1) H^⊗t on ancilla, (2) controlled-U^(2^k) operations, "
    "(3) inverse QFT on ancilla, (4) measure ancilla → φ to t bits. "
    "Precision: 2^(-t). Success probability: ≥ 4/π² ≈ 0.405 for t bits. "
    "Used in: Shor's algorithm, HHL, quantum chemistry (VQE energy estimation)."
),
},
{
"topic": "VQE",
"category": "QUANTUM_ALGORITHM",
"difficulty": "advanced",
"keywords": ["VQE", "variational quantum eigensolver", "ansatz", "NISQ", "chemistry"],
"body": (
    "VQE (Variational Quantum Eigensolver): hybrid quantum-classical algorithm for ground state energy. "
    "Variational principle: E_0 ≤ ⟨ψ(θ)|H|ψ(θ)⟩ for any |ψ(θ)⟩. "
    "Steps: (1) prepare parametric ansatz |ψ(θ)⟩ on quantum computer, "
    "(2) measure expectation value ⟨H⟩, "
    "(3) classical optimizer updates θ to minimize ⟨H⟩, "
    "(4) repeat until convergence. "
    "NISQ-friendly: shallow circuits. Used for quantum chemistry, materials science. "
    "Limitation: barren plateaus, local minima, measurement overhead."
),
},
{
"topic": "QAOA",
"category": "QUANTUM_ALGORITHM",
"difficulty": "advanced",
"keywords": ["QAOA", "quantum approximate optimization", "combinatorial", "MaxCut", "NISQ"],
"body": (
    "QAOA (Quantum Approximate Optimization Algorithm): solves combinatorial optimization. "
    "Alternates between problem Hamiltonian H_C and mixer Hamiltonian H_B = Σ X_i. "
    "Circuit: |ψ(γ,β)⟩ = e^(-iβ_p H_B) e^(-iγ_p H_C) ... e^(-iβ_1 H_B) e^(-iγ_1 H_C) |+⟩^n. "
    "p layers: deeper p → better approximation. p→∞ → exact solution. "
    "Classical optimizer finds optimal γ,β parameters. "
    "Applied to: MaxCut, TSP, portfolio optimization. NISQ-era algorithm."
),
},
{
"topic": "quantum teleportation",
"category": "QUANTUM_ALGORITHM",
"difficulty": "intermediate",
"keywords": ["teleportation", "bell measurement", "classical bits", "no-cloning", "transfer"],
"body": (
    "Quantum teleportation: transfers unknown qubit state |ψ⟩=α|0⟩+β|1⟩ using entanglement. "
    "Requires: 1 entangled Bell pair + 2 classical bits. Does NOT violate no-cloning. "
    "Steps: (1) Alice+Bob share |Φ+⟩, (2) Alice performs Bell measurement on |ψ⟩ and her half, "
    "(3) Alice sends 2 classical bits to Bob, "
    "(4) Bob applies correction (I/X/Z/XZ) based on bits → recovers |ψ⟩. "
    "Original state is destroyed at Alice (no cloning). "
    "Used in: quantum networks, quantum repeaters, distributed quantum computing."
),
},

# ── ERROR CORRECTION ──────────────────────────
{
"topic": "quantum error correction",
"category": "QUANTUM_ERROR_CORRECTION",
"difficulty": "advanced",
"keywords": ["error correction", "bit flip code", "phase flip", "shor code", "stabilizer", "syndrome"],
"body": (
    "Quantum errors: bit flip (X), phase flip (Z), or both (Y). "
    "3-qubit bit flip code: |0⟩→|000⟩, |1⟩→|111⟩. Corrects 1 bit flip. "
    "3-qubit phase flip code: uses Hadamard basis. "
    "Shor code: 9 qubits, corrects arbitrary single-qubit error. "
    "Stabilizer codes: defined by commuting Pauli operators (stabilizers). "
    "Surface code: leading practical QEC code, threshold ~1% error rate. "
    "Fault tolerance threshold: if physical error rate < threshold, logical error → 0."
),
},

# ── CRYPTOGRAPHY ──────────────────────────────
{
"topic": "quantum cryptography",
"category": "QUANTUM_CRYPTOGRAPHY",
"difficulty": "intermediate",
"keywords": ["QKD", "BB84", "quantum key distribution", "eavesdropping", "no-cloning"],
"body": (
    "BB84 (Bennett-Brassard 1984): first quantum key distribution protocol. "
    "Uses 4 states in 2 bases: {|0⟩,|1⟩} and {|+⟩,|-⟩}. "
    "Security: eavesdropping disturbs quantum states (no-cloning theorem). "
    "Steps: (1) Alice sends random qubits in random bases, "
    "(2) Bob measures in random bases, (3) sift matching bases → raw key, "
    "(4) error estimation detects eavesdropping, (5) privacy amplification → secure key. "
    "E91 protocol uses entangled pairs and Bell inequality violation for security."
),
},

# ── HARDWARE ──────────────────────────────────
{
"topic": "quantum hardware",
"category": "QUANTUM_HARDWARE",
"difficulty": "intermediate",
"keywords": ["superconducting", "trapped ion", "photonic", "spin qubit", "topological", "coherence time"],
"body": (
    "Superconducting qubits (IBM, Google): Josephson junction based. Fast gates (~ns). "
    "Coherence time: ~100μs. Connectivity limited. Operating temp: ~15mK. "
    "Trapped ions (IonQ, Honeywell): long coherence (~minutes). All-to-all connectivity. "
    "Slower gates (~μs). Photonic qubits: room temperature, hard to entangle. "
    "Spin qubits: silicon-based, small, long coherence. "
    "Key metrics: T1 (relaxation), T2 (dephasing), gate fidelity, qubit count, connectivity. "
    "NISQ era: 50-1000 noisy qubits, no full error correction."
),
},

# ── UNCERTAINTY & INTERFERENCE ────────────────
{
"topic": "heisenberg uncertainty principle",
"category": "QUANTUM_MECHANICS",
"difficulty": "intermediate",
"keywords": ["uncertainty", "heisenberg", "position", "momentum", "commutator"],
"body": (
    "Heisenberg uncertainty principle: ΔxΔp ≥ ℏ/2. "
    "General form: ΔAΔB ≥ |⟨[A,B]⟩|/2 for non-commuting observables A,B. "
    "Energy-time: ΔEΔt ≥ ℏ/2. "
    "Not a measurement limitation — fundamental property of quantum states. "
    "Commutator [X,P]=iℏ. Compatible observables commute: [A,B]=0 → can be simultaneously measured."
),
},
{
"topic": "quantum interference",
"category": "QUANTUM_MECHANICS",
"difficulty": "intermediate",
"keywords": ["interference", "constructive", "destructive", "amplitude", "double slit"],
"body": (
    "Quantum interference: amplitudes (not probabilities) add. "
    "Constructive: amplitudes reinforce → higher probability. "
    "Destructive: amplitudes cancel → lower/zero probability. "
    "Key to quantum speedup: algorithms amplify correct answer amplitudes, "
    "cancel wrong answer amplitudes. "
    "Example: Hadamard followed by Hadamard returns to |0⟩ — destructive interference cancels |1⟩ path."
),
},

# ── COMPLEXITY ────────────────────────────────
{
"topic": "quantum complexity",
"category": "QUANTUM_COMPUTING",
"difficulty": "advanced",
"keywords": ["BQP", "complexity", "P", "NP", "quantum advantage", "speedup"],
"body": (
    "BQP (Bounded-error Quantum Polynomial time): problems solvable by quantum computer in poly time. "
    "P ⊆ BQP. Believed: NP ⊄ BQP (quantum computers don't solve all NP problems). "
    "Quantum speedups: exponential (Shor, Simon), quadratic (Grover), polynomial (quantum simulation). "
    "Quantum supremacy: Google 2019 — 53-qubit Sycamore performed task in 200s vs ~10,000 years classical. "
    "Quantum advantage requires: coherence, entanglement, interference working together."
),
},
]

# ─────────────────────────────────────────────
# RETRIEVAL ENGINE
# ─────────────────────────────────────────────

def _score(entry: dict, query: str) -> float:
    q = query.lower()
    score = 0.0
    for kw in entry["keywords"]:
        if kw.lower() in q:
            score += 2.0
    if entry["topic"].lower() in q:
        score += 3.0
    words = re.findall(r'\w+', q)
    body_lower = entry["body"].lower()
    for w in words:
        if len(w) > 3 and w in body_lower:
            score += 0.3
    return score


def retrieve(query: str, top_k: int = 3, difficulty: Optional[str] = None) -> list[dict]:
    scored = [(e, _score(e, query)) for e in KNOWLEDGE_BASE]
    scored = [(e, s) for e, s in scored if s > 0]
    if difficulty and difficulty in ("beginner", "intermediate", "advanced"):
        level_map = {"beginner": 0, "intermediate": 1, "advanced": 2}
        user_level = level_map[difficulty]
        entry_level = {"beginner": 0, "intermediate": 1, "advanced": 2, "research": 3}
        scored = [(e, s + (0.5 if entry_level.get(e["difficulty"], 1) <= user_level else 0))
                  for e, s in scored]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [e for e, _ in scored[:top_k]]


def build_context_block(query: str, difficulty: str = "beginner") -> str:
    entries = retrieve(query, top_k=3, difficulty=difficulty)
    if not entries:
        return ""
    lines = ["VERIFIED QUANTUM KNOWLEDGE (use this to ground your answer):"]
    for e in entries:
        lines.append(f"\n[{e['category']} | {e['difficulty'].upper()}] {e['topic'].upper()}")
        lines.append(e["body"])
    return "\n".join(lines)
