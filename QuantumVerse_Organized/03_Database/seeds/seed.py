"""
Database seeder — populates learning modules, lessons, and quizzes.
Run: python -m app.database.seed
"""
import asyncio
from app.database.connection import engine, Base
from app.database.session import AsyncSessionLocal
from app.models.learning import LearningModule, Lesson
from app.models.quiz import Quiz, Question, Difficulty, QuestionType

MODULES = [
    {"title": "Quantum Fundamentals", "level": 1, "description": "Start your quantum journey from the very basics.", "icon": "atom", "lessons": [
        {"title": "Introduction to Quantum Computing", "xp_reward": 50, "estimated_minutes": 10, "content": {"blocks": [{"type": "text", "content": "Quantum computing harnesses quantum mechanics to solve problems classical computers cannot."}]}},
        {"title": "Classical vs Quantum Computing", "xp_reward": 50, "estimated_minutes": 12},
        {"title": "Bits vs Qubits", "xp_reward": 60, "estimated_minutes": 15},
        {"title": "Superposition", "xp_reward": 75, "estimated_minutes": 15},
        {"title": "Quantum Measurement", "xp_reward": 75, "estimated_minutes": 12},
        {"title": "Quantum States", "xp_reward": 80, "estimated_minutes": 15},
        {"title": "The Bloch Sphere", "xp_reward": 100, "estimated_minutes": 20},
    ]},
    {"title": "Quantum Gates", "level": 2, "description": "Learn the building blocks of quantum circuits.", "icon": "cpu", "lessons": [
        {"title": "Pauli-X Gate (Quantum NOT)", "xp_reward": 60, "estimated_minutes": 10},
        {"title": "Pauli-Y Gate", "xp_reward": 60, "estimated_minutes": 10},
        {"title": "Pauli-Z Gate", "xp_reward": 60, "estimated_minutes": 10},
        {"title": "Hadamard Gate", "xp_reward": 80, "estimated_minutes": 15},
        {"title": "Phase (S) Gate", "xp_reward": 70, "estimated_minutes": 12},
        {"title": "T Gate", "xp_reward": 70, "estimated_minutes": 12},
        {"title": "Rotation Gates (RX, RY, RZ)", "xp_reward": 90, "estimated_minutes": 20},
    ]},
    {"title": "Multi-Qubit Systems", "level": 3, "description": "Explore entanglement and multi-qubit operations.", "icon": "git-branch", "lessons": [
        {"title": "Multiple Qubits", "xp_reward": 80, "estimated_minutes": 15},
        {"title": "CNOT Gate", "xp_reward": 90, "estimated_minutes": 15},
        {"title": "Controlled Gates", "xp_reward": 90, "estimated_minutes": 15},
        {"title": "Quantum Entanglement", "xp_reward": 120, "estimated_minutes": 20},
        {"title": "Bell States", "xp_reward": 120, "estimated_minutes": 20},
    ]},
    {"title": "Quantum Algorithms", "level": 4, "description": "Discover the power of quantum algorithms.", "icon": "zap", "lessons": [
        {"title": "Deutsch-Jozsa Algorithm", "xp_reward": 150, "estimated_minutes": 25},
        {"title": "Grover's Search Algorithm", "xp_reward": 200, "estimated_minutes": 30},
        {"title": "Quantum Fourier Transform", "xp_reward": 200, "estimated_minutes": 30},
        {"title": "Shor's Algorithm (Overview)", "xp_reward": 250, "estimated_minutes": 35},
        {"title": "Quantum Teleportation", "xp_reward": 200, "estimated_minutes": 30},
        {"title": "Superdense Coding", "xp_reward": 150, "estimated_minutes": 25},
    ]},
]


SAMPLE_QUIZ = {
    "title": "Quantum Fundamentals Quiz",
    "difficulty": "easy",
    "xp_reward": 100,
    "questions": [
        {"question_text": "What is a qubit?", "question_type": "mcq", "options": [{"id": "a", "text": "A quantum bit that can be 0, 1, or both simultaneously"}, {"id": "b", "text": "A classical bit"}, {"id": "c", "text": "A type of quantum gate"}, {"id": "d", "text": "A quantum measurement device"}], "correct_answer": "a", "explanation": "A qubit is the quantum analog of a classical bit, existing in superposition of 0 and 1 until measured.", "topic": "fundamentals"},
        {"question_text": "What does the Hadamard gate do to a |0⟩ state?", "question_type": "mcq", "options": [{"id": "a", "text": "Flips to |1⟩"}, {"id": "b", "text": "Creates equal superposition of |0⟩ and |1⟩"}, {"id": "c", "text": "Leaves unchanged"}, {"id": "d", "text": "Measures the qubit"}], "correct_answer": "b", "explanation": "The Hadamard gate creates a superposition: H|0⟩ = (|0⟩ + |1⟩)/√2", "topic": "gates"},
        {"question_text": "Quantum entanglement means:", "question_type": "mcq", "options": [{"id": "a", "text": "Two qubits that always measure the same"}, {"id": "b", "text": "Two qubits are physically connected"}, {"id": "c", "text": "The quantum states of two qubits are correlated regardless of distance"}, {"id": "d", "text": "A qubit in superposition"}], "correct_answer": "c", "explanation": "Entanglement is a quantum correlation where measuring one qubit instantly determines the state of the other.", "topic": "fundamentals"},
        {"question_text": "The CNOT gate flips the target qubit when:", "question_type": "mcq", "options": [{"id": "a", "text": "Always"}, {"id": "b", "text": "Never"}, {"id": "c", "text": "Control qubit is |1⟩"}, {"id": "d", "text": "Control qubit is |0⟩"}], "correct_answer": "c", "explanation": "CNOT (Controlled-NOT) flips the target qubit only when the control qubit is in state |1⟩.", "topic": "gates"},
        {"question_text": "Quantum superposition collapses when:", "question_type": "mcq", "options": [{"id": "a", "text": "A gate is applied"}, {"id": "b", "text": "The qubit is measured"}, {"id": "c", "text": "Time passes"}, {"id": "d", "text": "Temperature increases"}], "correct_answer": "b", "explanation": "Measuring a qubit collapses its superposition into a definite classical state (0 or 1).", "topic": "fundamentals"},
    ]
}

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        # Seed modules and lessons
        for mod_data in MODULES:
            lessons_data = mod_data.pop("lessons", [])
            module = LearningModule(**mod_data, order_index=mod_data["level"])
            session.add(module)
            await session.flush()
            for i, ld in enumerate(lessons_data):
                lesson = Lesson(module_id=module.id, order_index=i, content=ld.pop("content", {}), **ld)
                session.add(lesson)
        # Seed sample quiz
        quiz_data = SAMPLE_QUIZ.copy()
        questions_data = quiz_data.pop("questions")
        quiz = Quiz(**quiz_data)
        session.add(quiz)
        await session.flush()
        for qd in questions_data:
            session.add(Question(quiz_id=quiz.id, **qd))
        await session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
