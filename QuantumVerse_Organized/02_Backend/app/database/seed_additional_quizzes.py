"""
Add the remaining 7 QuantumVerse quizzes.
The original Quantum Fundamentals Quiz already exists.
"""

import asyncio

from sqlalchemy import select

from app.database.session import AsyncSessionLocal
from app.models.learning import LearningModule
from app.models.quiz import Quiz, Question


QUIZZES = [
    {
        "title": "Qubit & Measurement Quiz",
        "level": 1,
        "difficulty": "easy",
        "xp_reward": 100,
        "questions": [
            {
                "question_text": "What is the main difference between a classical bit and a qubit?",
                "options": [
                    {"id": "a", "text": "A qubit can exist in a superposition of 0 and 1"},
                    {"id": "b", "text": "A qubit can only store the value 0"},
                    {"id": "c", "text": "A classical bit uses quantum mechanics"},
                    {"id": "d", "text": "There is no difference"},
                ],
                "correct_answer": "a",
                "explanation": "A qubit can exist in a quantum superposition of the basis states |0⟩ and |1⟩.",
                "topic": "qubits",
            },
            {
                "question_text": "What happens when a qubit in superposition is measured?",
                "options": [
                    {"id": "a", "text": "It remains in the same superposition"},
                    {"id": "b", "text": "It collapses to a definite measurement outcome"},
                    {"id": "c", "text": "It becomes two qubits"},
                    {"id": "d", "text": "It automatically becomes entangled"},
                ],
                "correct_answer": "b",
                "explanation": "Measurement produces a classical outcome and projects the qubit into the corresponding basis state.",
                "topic": "measurement",
            },
            {
                "question_text": "Which notation represents the computational basis state zero?",
                "options": [
                    {"id": "a", "text": "|1⟩"},
                    {"id": "b", "text": "|+⟩"},
                    {"id": "c", "text": "|0⟩"},
                    {"id": "d", "text": "|−⟩"},
                ],
                "correct_answer": "c",
                "explanation": "|0⟩ is one of the two computational basis states of a qubit.",
                "topic": "quantum_states",
            },
            {
                "question_text": "What does the Bloch sphere represent?",
                "options": [
                    {"id": "a", "text": "Only classical binary states"},
                    {"id": "b", "text": "The state of a single qubit geometrically"},
                    {"id": "c", "text": "A multi-qubit quantum computer"},
                    {"id": "d", "text": "A quantum measurement device"},
                ],
                "correct_answer": "b",
                "explanation": "The Bloch sphere provides a geometric representation of the pure state of a single qubit.",
                "topic": "bloch_sphere",
            },
            {
                "question_text": "If a qubit is measured in the computational basis, what are the possible outcomes?",
                "options": [
                    {"id": "a", "text": "Only 0"},
                    {"id": "b", "text": "Only 1"},
                    {"id": "c", "text": "0 or 1"},
                    {"id": "d", "text": "0, 1, 2, or 3"},
                ],
                "correct_answer": "c",
                "explanation": "A computational-basis measurement of a single qubit produces either 0 or 1.",
                "topic": "measurement",
            },
        ],
    },
    {
        "title": "Quantum Gates Quiz",
        "level": 2,
        "difficulty": "easy",
        "xp_reward": 100,
        "questions": [
            {
                "question_text": "Which gate acts like a quantum NOT operation?",
                "options": [
                    {"id": "a", "text": "X gate"},
                    {"id": "b", "text": "Z gate"},
                    {"id": "c", "text": "H gate"},
                    {"id": "d", "text": "S gate"},
                ],
                "correct_answer": "a",
                "explanation": "The Pauli-X gate swaps |0⟩ and |1⟩, making it the quantum equivalent of a NOT operation.",
                "topic": "pauli_x",
            },
            {
                "question_text": "What does the Pauli-Z gate primarily change?",
                "options": [
                    {"id": "a", "text": "The qubit's phase"},
                    {"id": "b", "text": "The number of qubits"},
                    {"id": "c", "text": "The measurement device"},
                    {"id": "d", "text": "The circuit width"},
                ],
                "correct_answer": "a",
                "explanation": "The Z gate leaves |0⟩ unchanged and introduces a phase of -1 to |1⟩.",
                "topic": "pauli_z",
            },
            {
                "question_text": "Which gate creates an equal superposition from |0⟩?",
                "options": [
                    {"id": "a", "text": "X"},
                    {"id": "b", "text": "H"},
                    {"id": "c", "text": "Z"},
                    {"id": "d", "text": "T"},
                ],
                "correct_answer": "b",
                "explanation": "H|0⟩ = (|0⟩ + |1⟩)/√2, creating an equal superposition.",
                "topic": "hadamard",
            },
            {
                "question_text": "Which of these is a single-qubit phase gate?",
                "options": [
                    {"id": "a", "text": "S gate"},
                    {"id": "b", "text": "CNOT gate"},
                    {"id": "c", "text": "SWAP gate"},
                    {"id": "d", "text": "Toffoli gate"},
                ],
                "correct_answer": "a",
                "explanation": "The S gate applies a phase shift to the |1⟩ component of a qubit.",
                "topic": "phase_gates",
            },
            {
                "question_text": "Quantum gates are generally represented mathematically by:",
                "options": [
                    {"id": "a", "text": "Probability tables only"},
                    {"id": "b", "text": "Unitary matrices"},
                    {"id": "c", "text": "Classical truth tables only"},
                    {"id": "d", "text": "Random numbers"},
                ],
                "correct_answer": "b",
                "explanation": "Quantum gates are represented by unitary operators that preserve the norm of a quantum state.",
                "topic": "quantum_gates",
            },
        ],
    },
    {
        "title": "Gate Operations Quiz",
        "level": 2,
        "difficulty": "medium",
        "xp_reward": 125,
        "questions": [
            {
                "question_text": "What is the effect of applying X twice to a qubit?",
                "options": [
                    {"id": "a", "text": "It measures the qubit"},
                    {"id": "b", "text": "It returns the qubit to its original state"},
                    {"id": "c", "text": "It creates entanglement"},
                    {"id": "d", "text": "It removes the qubit"},
                ],
                "correct_answer": "b",
                "explanation": "The Pauli-X gate is its own inverse, so X² = I.",
                "topic": "gate_operations",
            },
            {
                "question_text": "Which gate is commonly used to place |1⟩ into an equal superposition?",
                "options": [
                    {"id": "a", "text": "H"},
                    {"id": "b", "text": "X only"},
                    {"id": "c", "text": "Z only"},
                    {"id": "d", "text": "S only"},
                ],
                "correct_answer": "a",
                "explanation": "Applying H to |1⟩ produces (|0⟩ - |1⟩)/√2, an equal-magnitude superposition.",
                "topic": "hadamard",
            },
            {
                "question_text": "What does a rotation gate change?",
                "options": [
                    {"id": "a", "text": "The orientation of a qubit state"},
                    {"id": "b", "text": "The number of classical bits"},
                    {"id": "c", "text": "The database schema"},
                    {"id": "d", "text": "The number of measurement shots"},
                ],
                "correct_answer": "a",
                "explanation": "RX, RY, and RZ rotate a qubit state around the corresponding Bloch-sphere axis.",
                "topic": "rotation_gates",
            },
            {
                "question_text": "Which gate is associated with a phase rotation of π/4?",
                "options": [
                    {"id": "a", "text": "T gate"},
                    {"id": "b", "text": "X gate"},
                    {"id": "c", "text": "CNOT gate"},
                    {"id": "d", "text": "SWAP gate"},
                ],
                "correct_answer": "a",
                "explanation": "The T gate applies a phase of π/4 to the |1⟩ component.",
                "topic": "t_gate",
            },
            {
                "question_text": "Why must quantum gates be reversible?",
                "options": [
                    {"id": "a", "text": "Because ideal quantum evolution is unitary"},
                    {"id": "b", "text": "Because measurements are always reversible"},
                    {"id": "c", "text": "Because qubits cannot change state"},
                    {"id": "d", "text": "Because classical computers require it"},
                ],
                "correct_answer": "a",
                "explanation": "Closed-system quantum evolution is described by unitary operators, which have inverses.",
                "topic": "unitarity",
            },
        ],
    },
    {
        "title": "Entanglement & Bell States Quiz",
        "level": 3,
        "difficulty": "medium",
        "xp_reward": 150,
        "questions": [
            {
                "question_text": "What is quantum entanglement?",
                "options": [
                    {"id": "a", "text": "A classical communication protocol"},
                    {"id": "b", "text": "A strong quantum correlation between systems"},
                    {"id": "c", "text": "A type of single-qubit gate"},
                    {"id": "d", "text": "A measurement error"},
                ],
                "correct_answer": "b",
                "explanation": "Entangled quantum systems have joint states that cannot be described as independent states of each subsystem.",
                "topic": "entanglement",
            },
            {
                "question_text": "Which gate is commonly used with H to create a Bell state?",
                "options": [
                    {"id": "a", "text": "CNOT"},
                    {"id": "b", "text": "T"},
                    {"id": "c", "text": "Z only"},
                    {"id": "d", "text": "RX only"},
                ],
                "correct_answer": "a",
                "explanation": "H creates superposition on the first qubit and CNOT can then create entanglement between the two qubits.",
                "topic": "bell_states",
            },
            {
                "question_text": "How many qubits are required for a standard Bell state?",
                "options": [
                    {"id": "a", "text": "1"},
                    {"id": "b", "text": "2"},
                    {"id": "c", "text": "3"},
                    {"id": "d", "text": "4"},
                ],
                "correct_answer": "b",
                "explanation": "A Bell state is a maximally entangled state of two qubits.",
                "topic": "bell_states",
            },
            {
                "question_text": "What is a key property of entangled qubits?",
                "options": [
                    {"id": "a", "text": "Their joint state can show correlations not explained by independent states"},
                    {"id": "b", "text": "They must always be physically touching"},
                    {"id": "c", "text": "They cannot be measured"},
                    {"id": "d", "text": "They stop obeying quantum mechanics"},
                ],
                "correct_answer": "a",
                "explanation": "Entanglement creates correlations in the joint quantum state that cannot be represented as a simple product of individual states.",
                "topic": "entanglement",
            },
            {
                "question_text": "Which Bell state is represented by (|00⟩ + |11⟩)/√2?",
                "options": [
                    {"id": "a", "text": "Φ+"},
                    {"id": "b", "text": "Φ−"},
                    {"id": "c", "text": "Ψ+"},
                    {"id": "d", "text": "Ψ−"},
                ],
                "correct_answer": "a",
                "explanation": "The Bell state Φ+ is (|00⟩ + |11⟩)/√2.",
                "topic": "bell_states",
            },
        ],
    },
    {
        "title": "Multi-Qubit Operations Quiz",
        "level": 3,
        "difficulty": "medium",
        "xp_reward": 150,
        "questions": [
            {
                "question_text": "In a CNOT gate, what is the role of the control qubit?",
                "options": [
                    {"id": "a", "text": "It determines whether the target is flipped"},
                    {"id": "b", "text": "It is always measured first"},
                    {"id": "c", "text": "It is removed from the circuit"},
                    {"id": "d", "text": "It always becomes |1⟩"},
                ],
                "correct_answer": "a",
                "explanation": "CNOT applies an X operation to the target only when the control qubit is |1⟩.",
                "topic": "cnot",
            },
            {
                "question_text": "What happens to the target of CNOT when the control is |0⟩?",
                "options": [
                    {"id": "a", "text": "The target is flipped"},
                    {"id": "b", "text": "The target is unchanged"},
                    {"id": "c", "text": "The target is measured"},
                    {"id": "d", "text": "The target is deleted"},
                ],
                "correct_answer": "b",
                "explanation": "When the control is |0⟩, CNOT performs no operation on the target.",
                "topic": "cnot",
            },
            {
                "question_text": "How many computational basis states exist for 3 qubits?",
                "options": [
                    {"id": "a", "text": "3"},
                    {"id": "b", "text": "6"},
                    {"id": "c", "text": "8"},
                    {"id": "d", "text": "9"},
                ],
                "correct_answer": "c",
                "explanation": "n qubits have 2^n computational basis states, so 3 qubits have 8.",
                "topic": "multi_qubit",
            },
            {
                "question_text": "What operation exchanges the states of two qubits?",
                "options": [
                    {"id": "a", "text": "SWAP"},
                    {"id": "b", "text": "H"},
                    {"id": "c", "text": "T"},
                    {"id": "d", "text": "Z"},
                ],
                "correct_answer": "a",
                "explanation": "The SWAP gate exchanges the states of two qubits.",
                "topic": "swap",
            },
            {
                "question_text": "Why are multi-qubit systems powerful for quantum computing?",
                "options": [
                    {"id": "a", "text": "They provide a state space that grows exponentially with qubit count"},
                    {"id": "b", "text": "They eliminate all measurement"},
                    {"id": "c", "text": "They only store classical bits"},
                    {"id": "d", "text": "They prevent quantum interference"},
                ],
                "correct_answer": "a",
                "explanation": "n qubits have a state vector with 2^n computational-basis amplitudes.",
                "topic": "multi_qubit",
            },
        ],
    },
    {
        "title": "Quantum Algorithms Quiz",
        "level": 4,
        "difficulty": "medium",
        "xp_reward": 175,
        "questions": [
            {
                "question_text": "What is the main goal of Grover's algorithm?",
                "options": [
                    {"id": "a", "text": "Search an unstructured space faster than classical exhaustive search"},
                    {"id": "b", "text": "Factor large integers directly"},
                    {"id": "c", "text": "Transmit classical bits"},
                    {"id": "d", "text": "Create a physical qubit"},
                ],
                "correct_answer": "a",
                "explanation": "Grover's algorithm provides a quadratic speedup for searching an unstructured database.",
                "topic": "grover",
            },
            {
                "question_text": "What problem does Deutsch-Jozsa distinguish?",
                "options": [
                    {"id": "a", "text": "Constant functions from balanced functions"},
                    {"id": "b", "text": "Prime numbers from composite numbers"},
                    {"id": "c", "text": "Qubits from bits"},
                    {"id": "d", "text": "Entangled states from mixed states"},
                ],
                "correct_answer": "a",
                "explanation": "The Deutsch-Jozsa algorithm determines whether a promised function is constant or balanced.",
                "topic": "deutsch_jozsa",
            },
            {
                "question_text": "What is the Quantum Fourier Transform?",
                "options": [
                    {"id": "a", "text": "A quantum analogue of the discrete Fourier transform"},
                    {"id": "b", "text": "A measurement operation"},
                    {"id": "c", "text": "A classical sorting algorithm"},
                    {"id": "d", "text": "A type of qubit hardware"},
                ],
                "correct_answer": "a",
                "explanation": "QFT transforms amplitudes between computational and Fourier-like bases and is an important component of several quantum algorithms.",
                "topic": "qft",
            },
            {
                "question_text": "Which algorithm is associated with integer factorization?",
                "options": [
                    {"id": "a", "text": "Shor's algorithm"},
                    {"id": "b", "text": "Grover's algorithm"},
                    {"id": "c", "text": "Deutsch-Jozsa"},
                    {"id": "d", "text": "Bell-state preparation"},
                ],
                "correct_answer": "a",
                "explanation": "Shor's algorithm uses quantum period finding to factor integers efficiently in the idealized fault-tolerant setting.",
                "topic": "shor",
            },
            {
                "question_text": "Which concept allows quantum algorithms to amplify desired computational outcomes?",
                "options": [
                    {"id": "a", "text": "Interference"},
                    {"id": "b", "text": "Classical copying"},
                    {"id": "c", "text": "Data deletion"},
                    {"id": "d", "text": "Thermal noise"},
                ],
                "correct_answer": "a",
                "explanation": "Quantum interference can increase the amplitude of desired states while suppressing unwanted states.",
                "topic": "quantum_interference",
            },
        ],
    },
    {
        "title": "Quantum Search & Transform Quiz",
        "level": 4,
        "difficulty": "hard",
        "xp_reward": 200,
        "questions": [
            {
                "question_text": "What is the approximate query complexity of Grover's algorithm for an unstructured search of N items?",
                "options": [
                    {"id": "a", "text": "O(N)"},
                    {"id": "b", "text": "O(log N)"},
                    {"id": "c", "text": "O(√N)"},
                    {"id": "d", "text": "O(N²)"},
                ],
                "correct_answer": "c",
                "explanation": "Grover's algorithm requires O(√N) oracle queries, giving a quadratic improvement over classical exhaustive search.",
                "topic": "grover",
            },
            {
                "question_text": "What is the purpose of the oracle in Grover's algorithm?",
                "options": [
                    {"id": "a", "text": "Mark the desired solution states"},
                    {"id": "b", "text": "Measure every qubit"},
                    {"id": "c", "text": "Remove the search space"},
                    {"id": "d", "text": "Convert qubits into classical bits"},
                ],
                "correct_answer": "a",
                "explanation": "The oracle identifies the desired state by changing its phase, allowing amplitude amplification to increase its probability.",
                "topic": "grover",
            },
            {
                "question_text": "Which gate is fundamental to many QFT circuit constructions?",
                "options": [
                    {"id": "a", "text": "Controlled phase rotation"},
                    {"id": "b", "text": "Classical AND"},
                    {"id": "c", "text": "Measurement only"},
                    {"id": "d", "text": "Classical XOR only"},
                ],
                "correct_answer": "a",
                "explanation": "QFT circuits commonly use Hadamard gates together with controlled phase rotations.",
                "topic": "qft",
            },
            {
                "question_text": "What does the inverse QFT do?",
                "options": [
                    {"id": "a", "text": "Applies the inverse transformation of the QFT"},
                    {"id": "b", "text": "Measures all qubits"},
                    {"id": "c", "text": "Creates classical memory"},
                    {"id": "d", "text": "Deletes amplitudes"},
                ],
                "correct_answer": "a",
                "explanation": "The inverse QFT reverses the transformation performed by the Quantum Fourier Transform.",
                "topic": "qft",
            },
            {
                "question_text": "Why is quantum interference important in algorithms such as Grover's?",
                "options": [
                    {"id": "a", "text": "It can amplify amplitudes of desired states"},
                    {"id": "b", "text": "It prevents all measurements"},
                    {"id": "c", "text": "It turns qubits into bits"},
                    {"id": "d", "text": "It removes the need for gates"},
                ],
                "correct_answer": "a",
                "explanation": "Carefully designed interference increases the amplitude of useful states and decreases the amplitude of unwanted states.",
                "topic": "interference",
            },
        ],
    },
]


async def seed_additional_quizzes():
    async with AsyncSessionLocal() as session:
        modules_result = await session.execute(select(LearningModule))
        modules = modules_result.scalars().all()
        module_by_level = {m.level: m for m in modules}

        if len(module_by_level) < 4:
            raise RuntimeError(
                "Expected Levels 1-4 to exist before adding quizzes."
            )

        for quiz_data in QUIZZES:
            existing_result = await session.execute(
                select(Quiz).where(Quiz.title == quiz_data["title"])
            )
            existing = existing_result.scalar_one_or_none()

            if existing:
                print(f"Skipping existing quiz: {quiz_data['title']}")
                continue

            module = module_by_level[quiz_data["level"]]

            quiz = Quiz(
                title=quiz_data["title"],
                module_id=module.id,
                difficulty=quiz_data["difficulty"],
                xp_reward=quiz_data["xp_reward"],
            )
            session.add(quiz)
            await session.flush()

            for question_data in quiz_data["questions"]:
                session.add(
                    Question(
                        quiz_id=quiz.id,
                        question_text=question_data["question_text"],
                        question_type="mcq",
                        options=question_data["options"],
                        correct_answer=question_data["correct_answer"],
                        explanation=question_data["explanation"],
                        topic=question_data["topic"],
                    )
                )

            print(f"Added quiz: {quiz_data['title']}")

        await session.commit()

    print("Additional quizzes seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_additional_quizzes())
