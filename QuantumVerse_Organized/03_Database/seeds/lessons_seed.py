"""Lesson seed data — run once via seed.py"""

MODULES = [
    {
        "title": "Quantum Fundamentals",
        "description": "Master the building blocks of quantum computing from scratch.",
        "level": "beginner",
        "icon": "atom",
        "order_index": 1,
        "lessons": [
            {
                "title": "What is a Qubit?",
                "order_index": 1,
                "xp_reward": 50,
                "estimated_minutes": 8,
                "content": """
# What is a Qubit?

A **qubit** (quantum bit) is the fundamental unit of quantum information, the quantum analogue of a classical bit.

## Classical Bits vs Qubits

A classical bit is always in one of two definite states:
- `0` — off
- `1` — on

A qubit, however, can exist in a **superposition** of both states simultaneously. We write this using **Dirac notation** (ket notation):

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$

Where:
- $|0\rangle$ and $|1\rangle$ are the **basis states**
- $\alpha$ and $\beta$ are complex **probability amplitudes**
- The probabilities must sum to 1: $|\alpha|^2 + |\beta|^2 = 1$

## The Bloch Sphere

Every pure qubit state can be visualised as a point on the **Bloch sphere**:

- **North pole** → $|0\rangle$ (probability 1 of measuring 0)
- **South pole** → $|1\rangle$ (probability 1 of measuring 1)
- **Equator** → equal superposition states like $|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$

## Creating a Qubit in Qiskit

```python
from qiskit import QuantumCircuit

# Create a 1-qubit circuit
qc = QuantumCircuit(1, 1)

# Qubit starts in |0> by default
print(qc.draw())

# Apply Hadamard to create superposition
qc.h(0)
print("After H gate:", qc.draw())
```

## Key Takeaways

- Qubits are described by quantum state vectors
- Measurement **collapses** the superposition to 0 or 1 with probabilities $|\alpha|^2$ and $|\beta|^2$
- Before measurement, the qubit is genuinely in both states at once
- This is not like a coin — quantum superposition has measurable interference effects
""",
            },
            {
                "title": "Superposition & Measurement",
                "order_index": 2,
                "xp_reward": 60,
                "estimated_minutes": 10,
                "content": """
# Superposition & Measurement

## What is Quantum Superposition?

Superposition is one of the most counter-intuitive principles in quantum mechanics. Unlike classical probability ("the coin *is* heads, we just don't know"), a qubit in superposition is *genuinely* in multiple states simultaneously.

## The Hadamard Gate

The most common way to create superposition is the **Hadamard gate (H)**:

$$H = \frac{1}{\sqrt{2}}\begin{pmatrix}1 & 1 \\ 1 & -1\end{pmatrix}$$

Applied to $|0\rangle$:
$$H|0\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle) = |+\rangle$$

Applied to $|1\rangle$:
$$H|1\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle) = |-\rangle$$

## Measurement & Wave Function Collapse

When we **measure** a qubit:
1. The superposition collapses to $|0\rangle$ or $|1\rangle$
2. Probability of $|0\rangle$ = $|\alpha|^2$, probability of $|1\rangle$ = $|\beta|^2$
3. The original state is **destroyed** — you cannot clone an unknown quantum state

## Try It in Qiskit

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(1, 1)
qc.h(0)          # Create superposition
qc.measure(0, 0) # Measure

sim = AerSimulator()
result = sim.run(qc, shots=1000).result()
counts = result.get_counts()
print(counts)  # ~{'0': 500, '1': 500}
```

## The No-Cloning Theorem

You **cannot** copy an arbitrary unknown qubit state. This is the **quantum no-cloning theorem** and it has profound implications:
- Quantum states cannot be perfectly copied
- This is what makes quantum cryptography provably secure
- But it enables quantum teleportation!
""",
            },
            {
                "title": "Quantum Gates",
                "order_index": 3,
                "xp_reward": 80,
                "estimated_minutes": 12,
                "content": """
# Quantum Gates

Quantum gates are the quantum equivalent of classical logic gates. They are **unitary matrices** that transform qubit states reversibly.

## Single-Qubit Gates

### Pauli Gates

**X gate** (NOT gate): Flips $|0\rangle \leftrightarrow |1\rangle$
$$X = \begin{pmatrix}0 & 1 \\ 1 & 0\end{pmatrix}$$

**Y gate**: Combines X and Z with a phase
$$Y = \begin{pmatrix}0 & -i \\ i & 0\end{pmatrix}$$

**Z gate** (Phase flip): $|0\rangle \to |0\rangle$, $|1\rangle \to -|1\rangle$
$$Z = \begin{pmatrix}1 & 0 \\ 0 & -1\end{pmatrix}$$

### Phase Gates

**S gate** ($\sqrt{Z}$): 90° phase rotation on $|1\rangle$
**T gate** ($\sqrt{S}$): 45° phase rotation on $|1\rangle$ — essential for universality!

### Rotation Gates

Parametrised rotations around each Bloch sphere axis:
$$R_X(\theta) = e^{-i\theta X/2}, \quad R_Y(\theta) = e^{-i\theta Y/2}, \quad R_Z(\theta) = e^{-i\theta Z/2}$$

## Two-Qubit Gates

### CNOT (Controlled-NOT)
Flips the **target** qubit when the **control** qubit is $|1\rangle$:

$$CNOT = \begin{pmatrix}1&0&0&0 \\ 0&1&0&0 \\ 0&0&0&1 \\ 0&0&1&0\end{pmatrix}$$

Combining H + CNOT creates the **Bell state** (maximum entanglement):

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(2, 2)
qc.h(0)       # Superpose qubit 0
qc.cx(0, 1)   # Entangle qubit 1 with qubit 0
qc.measure_all()
# Result: only |00> and |11> — never |01> or |10>!
```

## Universality

Any quantum computation can be decomposed into:
- Single-qubit rotations ($R_X$, $R_Y$, $R_Z$)
- The CNOT gate

This is the quantum equivalent of NAND completeness in classical computing.
""",
            },
        ],
    },
    {
        "title": "Quantum Entanglement",
        "description": "Explore the spooky action at a distance and its computational power.",
        "level": "beginner",
        "icon": "link",
        "order_index": 2,
        "lessons": [
            {
                "title": "Bell States",
                "order_index": 1,
                "xp_reward": 100,
                "estimated_minutes": 12,
                "content": """
# Bell States

Bell states are the four **maximally entangled** two-qubit states. They form the cornerstone of quantum communication and cryptography.

## The Four Bell States

$$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$$
$$|\Phi^-\rangle = \frac{1}{\sqrt{2}}(|00\rangle - |11\rangle)$$
$$|\Psi^+\rangle = \frac{1}{\sqrt{2}}(|01\rangle + |10\rangle)$$
$$|\Psi^-\rangle = \frac{1}{\sqrt{2}}(|01\rangle - |10\rangle)$$

## Creating $|\Phi^+\rangle$

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)
qc.h(0)       # Hadamard on qubit 0
qc.cx(0, 1)   # CNOT: control=0, target=1
qc.measure([0,1], [0,1])

sim = AerSimulator()
counts = sim.run(qc, shots=1024).result().get_counts()
print(counts)  # {'00': ~512, '11': ~512}  — never 01 or 10!
```

## What Makes It Special?

In the Bell state $|\Phi^+\rangle$:
- If you measure qubit 0 and get **0**, qubit 1 is *instantly* **0**
- If you measure qubit 0 and get **1**, qubit 1 is *instantly* **1**
- This correlation is **perfect** regardless of the distance between qubits
- Einstein called this "spooky action at a distance"

## Bell's Theorem

John Bell proved in 1964 that these correlations **cannot be explained** by any classical hidden variable theory. Experimental tests (Aspect, 1982; Hensen, 2015) confirm: **quantum entanglement is real and non-local**.
""",
            },
        ],
    },
    {
        "title": "Quantum Algorithms",
        "description": "Learn the algorithms that give quantum computers their power.",
        "level": "intermediate",
        "icon": "cpu",
        "order_index": 3,
        "lessons": [
            {
                "title": "Grover's Algorithm",
                "order_index": 1,
                "xp_reward": 150,
                "estimated_minutes": 15,
                "content": """
# Grover's Search Algorithm

Grover's algorithm provides a **quadratic speedup** for searching an unstructured database.

## The Problem

Given an unsorted list of $N$ items with one marked item, find it.

- **Classical**: $O(N)$ queries (check each item)
- **Grover**: $O(\sqrt{N})$ queries

For $N = 10^6$: classical needs up to 1,000,000 checks; Grover needs ~1,000.

## How It Works

Grover's algorithm amplifies the amplitude of the target state through two operations:

### 1. The Oracle
Marks the target state $|x^*\rangle$ with a phase flip:
$$O|x\rangle = \begin{cases} -|x\rangle & \text{if } x = x^* \\ |x\rangle & \text{otherwise} \end{cases}$$

### 2. The Diffusion Operator
Reflects all amplitudes about the average:
$$D = 2|+\rangle\langle+| - I$$

Each iteration of Oracle + Diffusion **increases** the target amplitude by $\sim \frac{2}{\sqrt{N}}$.

After $k = \frac{\pi}{4}\sqrt{N}$ iterations, the probability peaks near 1.

## Qiskit Implementation

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import math

def grover_circuit(n: int, target: int) -> QuantumCircuit:
    qc = QuantumCircuit(n, n)
    qc.h(range(n))  # Equal superposition
    
    iterations = round(math.pi / 4 * math.sqrt(2**n))
    for _ in range(iterations):
        # Oracle: phase-flip target state
        target_bits = format(target, f"0{n}b")
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)
        
        # Diffusion operator
        qc.h(range(n))
        qc.x(range(n))
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
        qc.x(range(n))
        qc.h(range(n))
    
    qc.measure(range(n), range(n))
    return qc

qc = grover_circuit(3, 5)  # Find item 5 in 8-item list
sim = AerSimulator()
counts = sim.run(qc, shots=1024).result().get_counts()
print(counts)  # {"101": ~950, ...rest tiny}
```
""",
            },
        ],
    },
]


def get_seed_data():
    return MODULES
