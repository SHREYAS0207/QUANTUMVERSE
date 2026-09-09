import os

BASE = "/data/quantumverse"

files = {}

# ─── BACKEND MODELS ───────────────────────────────────────────────────────────
files["backend/app/models/user.py"] = '''
import uuid
from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Boolean, Enum, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base
import enum

class LearningLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    circuits: Mapped[list["Circuit"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    statistics: Mapped["UserStatistics"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    learning_level: Mapped[LearningLevel] = mapped_column(Enum(LearningLevel), default=LearningLevel.beginner)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    streak_days: Mapped[int] = mapped_column(Integer, default=0)
    last_active_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    user: Mapped["User"] = relationship(back_populates="profile")

class UserStatistics(Base):
    __tablename__ = "user_statistics"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    total_lessons_completed: Mapped[int] = mapped_column(Integer, default=0)
    total_circuits_created: Mapped[int] = mapped_column(Integer, default=0)
    total_simulations_run: Mapped[int] = mapped_column(Integer, default=0)
    total_quizzes_taken: Mapped[int] = mapped_column(Integer, default=0)
    total_quiz_accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    total_time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user: Mapped["User"] = relationship(back_populates="statistics")
'''

files["backend/app/models/circuit.py"] = '''
import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

class Circuit(Base):
    __tablename__ = "circuits"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    qubits: Mapped[int] = mapped_column(Integer, default=1)
    classical_bits: Mapped[int] = mapped_column(Integer, default=0)
    circuit_data: Mapped[dict] = mapped_column(JSON, default=dict)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False)
    template_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user: Mapped["User"] = relationship(back_populates="circuits")
    simulations: Mapped[list["SimulationHistory"]] = relationship(back_populates="circuit", cascade="all, delete-orphan")

class SimulationHistory(Base):
    __tablename__ = "simulation_history"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    circuit_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("circuits.id"), nullable=True)
    input_data: Mapped[dict] = mapped_column(JSON, default=dict)
    result_data: Mapped[dict] = mapped_column(JSON, default=dict)
    execution_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    shots: Mapped[int] = mapped_column(Integer, default=1024)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    circuit: Mapped["Circuit | None"] = relationship(back_populates="simulations")
'''

files["backend/app/models/learning.py"] = '''
import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, JSON, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base
import enum

class ProgressStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"

class LearningModule(Base):
    __tablename__ = "learning_modules"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    level: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-4
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    icon: Mapped[str] = mapped_column(String(50), default="atom")
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order_index")

class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    module_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learning_modules.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    xp_reward: Mapped[int] = mapped_column(Integer, default=50)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=10)
    module: Mapped["LearningModule"] = relationship(back_populates="lessons")
    progress: Mapped[list["LessonProgress"]] = relationship(back_populates="lesson", cascade="all, delete-orphan")

class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    status: Mapped[ProgressStatus] = mapped_column(Enum(ProgressStatus), default=ProgressStatus.not_started)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    lesson: Mapped["Lesson"] = relationship(back_populates="progress")
'''

files["backend/app/models/quiz.py"] = '''
import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Text, JSON, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base
import enum

class Difficulty(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class QuestionType(str, enum.Enum):
    mcq = "mcq"
    true_false = "true_false"
    circuit_predict = "circuit_predict"
    gate_identify = "gate_identify"

class Quiz(Base):
    __tablename__ = "quizzes"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    module_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("learning_modules.id"), nullable=True)
    difficulty: Mapped[Difficulty] = mapped_column(Enum(Difficulty), default=Difficulty.easy)
    time_limit_seconds: Mapped[int] = mapped_column(Integer, default=600)
    xp_reward: Mapped[int] = mapped_column(Integer, default=100)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    questions: Mapped[list["Question"]] = relationship(back_populates="quiz", cascade="all, delete-orphan")
    attempts: Mapped[list["QuizAttempt"]] = relationship(back_populates="quiz", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quizzes.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(Enum(QuestionType), default=QuestionType.mcq)
    options: Mapped[list] = mapped_column(JSON, default=list)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, default="")
    difficulty: Mapped[Difficulty] = mapped_column(Enum(Difficulty), default=Difficulty.easy)
    topic: Mapped[str] = mapped_column(String(100), default="")
    quiz: Mapped["Quiz"] = relationship(back_populates="questions")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    quiz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quizzes.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0)
    accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, default=0)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    quiz: Mapped["Quiz"] = relationship(back_populates="attempts")
    answers: Mapped[list["QuizAnswer"]] = relationship(back_populates="attempt", cascade="all, delete-orphan")

class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quiz_attempts.id"), nullable=False)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id"), nullable=False)
    user_answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, default=0)
    attempt: Mapped["QuizAttempt"] = relationship(back_populates="answers")
'''

files["backend/app/models/achievement.py"] = '''
import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

class Achievement(Base):
    __tablename__ = "achievements"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    icon: Mapped[str] = mapped_column(String(100), default="trophy")
    badge_color: Mapped[str] = mapped_column(String(50), default="gold")
    unlock_condition: Mapped[dict] = mapped_column(JSON, default=dict)
    xp_reward: Mapped[int] = mapped_column(Integer, default=100)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    user_achievements: Mapped[list["UserAchievement"]] = relationship(back_populates="achievement")

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    achievement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("achievements.id"), nullable=False)
    unlocked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    achievement: Mapped["Achievement"] = relationship(back_populates="user_achievements")
'''

files["backend/app/models/ai.py"] = '''
import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, Text, JSON, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base
import enum

class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"

class AIConversation(Base):
    __tablename__ = "ai_conversations"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), default="New Conversation")
    context: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    messages: Mapped[list["AIMessage"]] = relationship(back_populates="conversation", cascade="all, delete-orphan", order_by="AIMessage.created_at")

class AIMessage(Base):
    __tablename__ = "ai_messages"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_conversations.id"), nullable=False)
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    conversation: Mapped["AIConversation"] = relationship(back_populates="messages")
'''

# ─── BACKEND SCHEMAS ──────────────────────────────────────────────────────────
files["backend/app/schemas/__init__.py"] = '# schemas package\n'

files["backend/app/schemas/auth.py"] = '''
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import uuid

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    learning_level: str = "beginner"

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

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

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    learning_level: Optional[str] = None
    avatar_url: Optional[str] = None
'''

files["backend/app/schemas/circuit.py"] = '''
from pydantic import BaseModel
from typing import Optional, List, Any
import uuid
from datetime import datetime

class GateOperation(BaseModel):
    id: Optional[str] = None
    gate: str
    targets: List[int]
    controls: List[int] = []
    column: int
    params: Optional[dict] = None

class CircuitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    qubits: int = 1
    classical_bits: int = 0
    circuit_data: dict = {}

class CircuitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    qubits: Optional[int] = None
    classical_bits: Optional[int] = None
    circuit_data: Optional[dict] = None

class CircuitResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: Optional[str]
    qubits: int
    classical_bits: int
    circuit_data: dict
    is_template: bool
    template_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
'''

files["backend/app/schemas/simulation.py"] = '''
from pydantic import BaseModel
from typing import Optional, List

class SimulationRequest(BaseModel):
    qubits: int
    operations: List[dict]
    shots: int = 1024
    circuit_id: Optional[str] = None

class StepRequest(BaseModel):
    qubits: int
    operations: List[dict]
    step_index: int

class SimulationResult(BaseModel):
    success: bool
    counts: dict
    probabilities: dict
    execution_time: float
    total_shots: int
    state_vector: Optional[List] = None
    error: Optional[str] = None

class StepResult(BaseModel):
    success: bool
    step_index: int
    gate_applied: str
    state_description: str
    state_vector: List
    probabilities: dict
    explanation: str
    error: Optional[str] = None
'''

files["backend/app/schemas/ai.py"] = '''
from pydantic import BaseModel
from typing import Optional, List

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[dict] = None
    difficulty: str = "beginner"

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tokens_used: Optional[int] = None

class ExplainCircuitRequest(BaseModel):
    circuit_data: dict
    difficulty: str = "beginner"

class ExplainCircuitResponse(BaseModel):
    explanation: str
    gate_explanations: List[dict]
    expected_output: str
    suggestions: List[str]
'''

# ─── QUANTUM ENGINE ───────────────────────────────────────────────────────────
files["backend/app/quantum/__init__.py"] = '# quantum package\n'

files["backend/app/quantum/engine.py"] = '''
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from typing import List, Optional
import math


class CircuitBuilder:
    """Converts frontend JSON circuit description into a Qiskit QuantumCircuit."""

    SINGLE_QUBIT_GATES = {"X", "Y", "Z", "H", "S", "T", "SDG", "TDG"}
    ROTATION_GATES = {"RX", "RY", "RZ", "P"}
    TWO_QUBIT_GATES = {"CNOT", "CX", "CZ", "SWAP"}
    THREE_QUBIT_GATES = {"CCX", "TOFFOLI"}

    def build(self, qubits: int, classical_bits: int, operations: List[dict]) -> QuantumCircuit:
        qr = QuantumRegister(qubits, "q")
        if classical_bits > 0:
            cr = ClassicalRegister(classical_bits, "c")
            qc = QuantumCircuit(qr, cr)
        else:
            qc = QuantumCircuit(qr)

        for op in sorted(operations, key=lambda x: x.get("column", 0)):
            self._apply_gate(qc, op, qubits, classical_bits)

        return qc

    def _apply_gate(self, qc: QuantumCircuit, op: dict, n_qubits: int, n_classical: int) -> None:
        gate = op.get("gate", "").upper()
        targets = op.get("targets", [])
        controls = op.get("controls", [])
        params = op.get("params", {})

        if not targets and gate not in {"BARRIER"}:
            return

        try:
            if gate in self.SINGLE_QUBIT_GATES:
                method = getattr(qc, gate.lower(), None)
                if method:
                    method(targets[0])
            elif gate in self.ROTATION_GATES:
                angle = params.get("angle", math.pi / 2) if params else math.pi / 2
                method = getattr(qc, gate.lower(), None)
                if method:
                    method(angle, targets[0])
            elif gate in {"CNOT", "CX"}:
                if controls:
                    qc.cx(controls[0], targets[0])
            elif gate == "CZ":
                if controls:
                    qc.cz(controls[0], targets[0])
            elif gate == "SWAP":
                if len(targets) >= 2:
                    qc.swap(targets[0], targets[1])
            elif gate in {"CCX", "TOFFOLI"}:
                if len(controls) >= 2:
                    qc.ccx(controls[0], controls[1], targets[0])
            elif gate == "MEASURE":
                for i, t in enumerate(targets):
                    if i < n_classical:
                        qc.measure(t, i)
            elif gate == "BARRIER":
                qc.barrier()
        except Exception as e:
            print(f"[CircuitBuilder] Error applying gate {gate}: {e}")
'''

files["backend/app/quantum/simulator.py"] = '''
from qiskit_aer import AerSimulator
from qiskit import transpile
from qiskit.quantum_info import Statevector
from app.quantum.engine import CircuitBuilder
import time
from typing import Optional


class QuantumSimulator:
    """Runs quantum circuits using Qiskit Aer."""

    def __init__(self):
        self.simulator = AerSimulator()
        self.builder = CircuitBuilder()

    def run(self, qubits: int, operations: list, shots: int = 1024, classical_bits: Optional[int] = None) -> dict:
        n_classical = classical_bits if classical_bits is not None else qubits
        start = time.time()
        try:
            qc = self.builder.build(qubits, n_classical, operations)
            has_measure = any(op.get("gate", "").upper() == "MEASURE" for op in operations)
            if not has_measure:
                qc.measure_all()
            transpiled = transpile(qc, self.simulator)
            job = self.simulator.run(transpiled, shots=shots)
            result = job.result()
            counts = result.get_counts()
            total = sum(counts.values())
            probabilities = {k: v / total for k, v in counts.items()}
            elapsed = round((time.time() - start) * 1000, 2)
            return {
                "success": True,
                "counts": counts,
                "probabilities": probabilities,
                "execution_time": elapsed,
                "total_shots": total,
            }
        except Exception as e:
            return {"success": False, "counts": {}, "probabilities": {}, "execution_time": 0, "total_shots": 0, "error": str(e)}

    def get_statevector(self, qubits: int, operations: list) -> dict:
        """Get statevector without measurement."""
        try:
            ops_no_measure = [op for op in operations if op.get("gate", "").upper() != "MEASURE"]
            qc = self.builder.build(qubits, 0, ops_no_measure)
            sv = Statevector(qc)
            amplitudes = sv.data.tolist()
            probs = sv.probabilities_dict()
            return {"success": True, "amplitudes": [[a.real, a.imag] for a in amplitudes], "probabilities": probs}
        except Exception as e:
            return {"success": False, "error": str(e)}
'''

files["backend/app/quantum/step_executor.py"] = '''
from qiskit.quantum_info import Statevector
from app.quantum.engine import CircuitBuilder
import math


GATE_EXPLANATIONS = {
    "H": "Hadamard gate applied — qubit enters superposition. Now it has equal probability of being |0⟩ or |1⟩.",
    "X": "Pauli-X gate (quantum NOT) applied — qubit flipped from |0⟩ to |1⟩ or vice versa.",
    "Y": "Pauli-Y gate applied — combines X and Z rotations with a phase shift.",
    "Z": "Pauli-Z gate applied — flips the phase of the |1⟩ state (no visible change in measurement probabilities).",
    "S": "S gate applied — adds a 90° (π/2) phase rotation to the |1⟩ component.",
    "T": "T gate applied — adds a 45° (π/4) phase rotation, essential for universal quantum computation.",
    "CNOT": "CNOT (Controlled-NOT) applied — target qubit flips only if control qubit is |1⟩. This creates entanglement!",
    "CX": "CNOT applied — controlled-X operation creates entanglement between qubits.",
    "CZ": "Controlled-Z applied — applies Z gate to target only when control is |1⟩.",
    "SWAP": "SWAP gate applied — exchanges the quantum states of two qubits.",
    "CCX": "Toffoli (CCX) gate applied — target flips only if both control qubits are |1⟩.",
    "RX": "RX rotation applied — rotates the qubit state around the X-axis of the Bloch sphere.",
    "RY": "RY rotation applied — rotates around the Y-axis of the Bloch sphere.",
    "RZ": "RZ rotation applied — rotates around the Z-axis, adding a relative phase.",
    "MEASURE": "Measurement performed — quantum state collapses to a definite classical bit (0 or 1).",
}


class StepExecutor:
    def __init__(self):
        self.builder = CircuitBuilder()

    def execute_step(self, qubits: int, operations: list, step_index: int) -> dict:
        """Return quantum state after applying operations up to step_index."""
        try:
            ops_up_to = [
                op for op in operations
                if op.get("column", 0) <= step_index and op.get("gate", "").upper() != "MEASURE"
            ]
            qc = self.builder.build(qubits, 0, ops_up_to)
            sv = Statevector(qc)
            probs = sv.probabilities_dict()
            amplitudes = [[a.real, a.imag] for a in sv.data.tolist()]

            # Current gate at this step
            current_ops = [op for op in operations if op.get("column", 0) == step_index]
            gate_name = current_ops[0].get("gate", "UNKNOWN").upper() if current_ops else "UNKNOWN"
            explanation = GATE_EXPLANATIONS.get(gate_name, f"{gate_name} gate applied.")

            state_desc = self._format_state(sv.data.tolist(), qubits)

            return {
                "success": True,
                "step_index": step_index,
                "gate_applied": gate_name,
                "state_description": state_desc,
                "state_vector": amplitudes,
                "probabilities": probs,
                "explanation": explanation,
            }
        except Exception as e:
            return {"success": False, "step_index": step_index, "error": str(e), "gate_applied": "", "state_description": "", "state_vector": [], "probabilities": {}, "explanation": ""}

    def _format_state(self, amplitudes: list, qubits: int) -> str:
        """Format state vector as a human-readable ket notation."""
        terms = []
        for i, amp in enumerate(amplitudes):
            magnitude = math.sqrt(amp.real**2 + amp.imag**2) if hasattr(amp, "real") else abs(amp)
            if magnitude > 0.001:
                ket = format(i, f"0{qubits}b")
                coeff = f"{magnitude:.3f}"
                terms.append(f"{coeff}|{ket}⟩")
        return " + ".join(terms) if terms else "|0⟩"
'''

files["backend/app/quantum/algorithms/__init__.py"] = '# algorithms package\n'

files["backend/app/quantum/algorithms/grover.py"] = '''
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit import transpile
import math


def build_grover_circuit(n_qubits: int, target: int, iterations: int = None) -> dict:
    """Build and simulate Grover\'s search algorithm."""
    if n_qubits < 1:
        raise ValueError("Need at least 1 qubit")
    optimal_iter = max(1, round(math.pi / 4 * math.sqrt(2 ** n_qubits)))
    if iterations is None:
        iterations = optimal_iter

    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))

    for _ in range(iterations):
        # Oracle: mark target state
        target_bits = format(target, f"0{n_qubits}b")
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)
        qc.h(n_qubits - 1)
        if n_qubits > 1:
            qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)
        for i, bit in enumerate(reversed(target_bits)):
            if bit == "0":
                qc.x(i)

        # Diffusion operator
        qc.h(range(n_qubits))
        qc.x(range(n_qubits))
        qc.h(n_qubits - 1)
        if n_qubits > 1:
            qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)
        qc.x(range(n_qubits))
        qc.h(range(n_qubits))

    qc.measure(range(n_qubits), range(n_qubits))
    sim = AerSimulator()
    result = sim.run(transpile(qc, sim), shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    probs = {k: round(v / total, 4) for k, v in counts.items()}
    target_key = format(target, f"0{n_qubits}b")
    return {
        "success": True,
        "counts": counts,
        "probabilities": probs,
        "target": target_key,
        "target_probability": probs.get(target_key, 0),
        "iterations_used": iterations,
        "optimal_iterations": optimal_iter,
        "n_states": 2 ** n_qubits,
        "classical_complexity": f"O(N) = O({2**n_qubits})",
        "quantum_complexity": f"O(√N) ≈ O({round(math.sqrt(2**n_qubits), 1)})",
    }
'''

files["backend/app/quantum/algorithms/teleportation.py"] = '''
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile


def build_teleportation_circuit(state: str = "plus") -> dict:
    """Quantum teleportation of a single qubit state."""
    qc = QuantumCircuit(3, 3)
    # Step 1: Prepare state to teleport on qubit 0
    if state == "plus":
        qc.h(0)
    elif state == "minus":
        qc.x(0)
        qc.h(0)
    elif state == "one":
        qc.x(0)
    # else: leave |0⟩
    qc.barrier()
    # Step 2: Create Bell pair between qubits 1 and 2
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()
    # Step 3: Bell measurement on qubits 0 and 1
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.barrier()
    # Step 4: Classical corrections on qubit 2
    with qc.if_else((qc.clbits[1], 1)):
        qc.x(2)
    with qc.if_else((qc.clbits[0], 1)):
        qc.z(2)
    qc.measure(2, 2)

    sim = AerSimulator()
    result = sim.run(transpile(qc, sim), shots=1024).result()
    counts = result.get_counts()
    steps = [
        {"step": 1, "description": "Prepare input qubit state", "state": state},
        {"step": 2, "description": "Create Bell entangled pair (qubits 1,2)"},
        {"step": 3, "description": "Apply CNOT + Hadamard (Bell measurement)"},
        {"step": 4, "description": "Measure qubits 0 and 1"},
        {"step": 5, "description": "Apply conditional corrections to qubit 2"},
        {"step": 6, "description": "Qubit state successfully teleported!"},
    ]
    return {"success": True, "counts": counts, "steps": steps, "input_state": state, "circuit_qubits": 3}
'''

files["backend/app/quantum/algorithms/deutsch_jozsa.py"] = '''
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile


def build_deutsch_jozsa_circuit(oracle_type: str = "balanced", n_qubits: int = 3) -> dict:
    """Deutsch-Jozsa algorithm determining constant vs balanced functions."""
    total = n_qubits + 1
    qc = QuantumCircuit(total, n_qubits)
    # Initialize ancilla to |1⟩
    qc.x(n_qubits)
    qc.h(range(total))
    qc.barrier()
    # Oracle
    if oracle_type == "constant_one":
        qc.x(n_qubits)  # f(x) = 1 for all x
    elif oracle_type == "constant_zero":
        pass  # f(x) = 0 for all x, do nothing
    else:  # balanced: flip ancilla for first half of inputs
        for i in range(n_qubits):
            qc.cx(i, n_qubits)
    qc.barrier()
    qc.h(range(n_qubits))
    qc.measure(range(n_qubits), range(n_qubits))
    sim = AerSimulator()
    result = sim.run(transpile(qc, sim), shots=1024).result()
    counts = result.get_counts()
    all_zeros = "0" * n_qubits
    is_constant = all_zeros in counts and counts[all_zeros] > 900
    return {
        "success": True,
        "oracle_type": oracle_type,
        "result": "constant" if is_constant else "balanced",
        "is_correct": is_constant == oracle_type.startswith("constant"),
        "counts": counts,
        "n_qubits": n_qubits,
        "classical_queries_needed": 2 ** (n_qubits - 1) + 1,
        "quantum_queries_needed": 1,
    }
'''

files["backend/app/quantum/algorithms/qft.py"] = '''
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import math


def build_qft_circuit(n_qubits: int = 3, input_state: int = 0) -> dict:
    """Quantum Fourier Transform."""
    qc = QuantumCircuit(n_qubits)
    # Prepare input state
    if input_state > 0:
        bits = format(input_state % (2 ** n_qubits), f"0{n_qubits}b")
        for i, b in enumerate(reversed(bits)):
            if b == "1":
                qc.x(i)
    qc.barrier()
    # QFT circuit
    for i in range(n_qubits):
        qc.h(i)
        for j in range(i + 1, n_qubits):
            angle = math.pi / (2 ** (j - i))
            qc.cp(angle, j, i)
    for i in range(n_qubits // 2):
        qc.swap(i, n_qubits - 1 - i)
    sv = Statevector(qc)
    probs = {k: round(v, 4) for k, v in sv.probabilities_dict().items()}
    amplitudes = [[a.real, a.imag] for a in sv.data.tolist()]
    return {
        "success": True,
        "n_qubits": n_qubits,
        "input_state": input_state,
        "probabilities": probs,
        "amplitudes": amplitudes,
        "description": f"QFT of |{input_state}⟩ using {n_qubits} qubits",
    }
'''

# ─── AI SERVICE ───────────────────────────────────────────────────────────────
files["backend/app/ai/__init__.py"] = '# ai package\n'

files["backend/app/ai/prompts.py"] = '''
SYSTEM_PROMPT = """
You are QubitAI, an expert quantum computing educator built into QuantumVerse AI.
Your mission: make quantum computing accessible and exciting.

Rules:
- Always adapt explanations to the user\'s difficulty level.
- BEGINNER: Use simple analogies, avoid heavy math, be encouraging.
- INTERMEDIATE: Introduce math notation gradually, explain gate matrices briefly.
- ADVANCED: Use rigorous quantum formalism, Dirac notation, matrix representations.
- Keep answers concise but complete. Use examples always.
- When explaining circuits, describe what each gate does to the quantum state step by step.
- Never be condescending. Every question is valid.
- Use ⟨ ⟩ for bra-ket notation, | for kets.
"""

CIRCUIT_EXPLAIN_PROMPT = """
Analyze this quantum circuit and explain it clearly.
Circuit JSON: {circuit_json}
User level: {difficulty}

Provide:
1. What this circuit does overall
2. What each gate does step by step
3. Expected measurement outcomes
4. Any interesting quantum phenomena demonstrated
5. One suggestion to improve or extend the circuit

Be specific, not generic.
"""

QUIZ_GENERATION_PROMPT = """
Generate {count} multiple-choice quiz questions about quantum computing.
Topic: {topic}
Difficulty: {difficulty}

Return valid JSON array:
[
  {{
    "question_text": "...",
    "options": [{{"id": "a", "text": "..."}}, ...],
    "correct_answer": "a",
    "explanation": "...",
    "topic": "{topic}"
  }}
]

Make questions practical and conceptual, not just definitions.
"""
'''

files["backend/app/ai/provider.py"] = '''
import httpx
from app.core.config import settings
from app.ai.prompts import SYSTEM_PROMPT, CIRCUIT_EXPLAIN_PROMPT, QUIZ_GENERATION_PROMPT
from typing import List, Optional
import json


class LLMProvider:
    """Abstraction layer for LLM API calls. Supports OpenRouter and compatible APIs."""

    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.AI_MODEL
        self.base_url = settings.AI_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://quantumverse-ai.app",
            "X-Title": "QuantumVerse AI",
        }

    async def chat(self, messages: List[dict], difficulty: str = "beginner") -> str:
        system = SYSTEM_PROMPT + f"\n\nCurrent user level: {difficulty.upper()}"
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}] + messages,
            "max_tokens": 1024,
            "temperature": 0.7,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    async def explain_circuit(self, circuit_data: dict, difficulty: str = "beginner") -> dict:
        prompt = CIRCUIT_EXPLAIN_PROMPT.format(circuit_json=json.dumps(circuit_data, indent=2), difficulty=difficulty)
        response = await self.chat([{"role": "user", "content": prompt}], difficulty)
        return {"explanation": response, "gate_explanations": [], "expected_output": "", "suggestions": []}

    async def generate_quiz(self, topic: str, difficulty: str, count: int = 5) -> list:
        prompt = QUIZ_GENERATION_PROMPT.format(topic=topic, difficulty=difficulty, count=count)
        response = await self.chat([{"role": "user", "content": prompt}], difficulty)
        try:
            start = response.find("[")
            end = response.rfind("]") + 1
            return json.loads(response[start:end])
        except Exception:
            return []


llm = LLMProvider()
'''

# ─── API ROUTES ───────────────────────────────────────────────────────────────
files["backend/app/api/__init__.py"] = '# api package\n'
files["backend/app/api/v1/__init__.py"] = '# v1 package\n'

files["backend/app/api/v1/router.py"] = '''
from fastapi import APIRouter
from app.api.v1 import auth, circuits, simulation, learning, ai_tutor, quiz, achievements, algorithms

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(circuits.router, prefix="/circuits", tags=["Circuits"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["Simulation"])
api_router.include_router(learning.router, prefix="/learning", tags=["Learning"])
api_router.include_router(ai_tutor.router, prefix="/ai", tags=["AI Tutor"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
api_router.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
api_router.include_router(algorithms.router, prefix="/algorithms", tags=["Algorithms"])
'''

files["backend/app/api/v1/auth.py"] = '''
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_session
from app.models.user import User, Profile, UserStatistics
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, ProfileUpdateRequest
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.dependencies import get_current_user, get_db
import uuid

router = APIRouter()

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == request.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=request.email, name=request.name, hashed_password=get_password_hash(request.password))
    db.add(user)
    await db.flush()
    profile = Profile(id=user.id, learning_level=request.learning_level)
    stats = UserStatistics(user_id=user.id)
    db.add(profile)
    db.add(stats)
    await db.commit()
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token, user_id=str(user.id), name=user.name, email=user.email, learning_level=request.learning_level)

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    await db.execute(select(Profile).where(Profile.id == user.id))
    profile_res = await db.execute(select(Profile).where(Profile.id == user.id))
    profile = profile_res.scalar_one_or_none()
    level = profile.learning_level if profile else "beginner"
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token, user_id=str(user.id), name=user.name, email=user.email, learning_level=level)

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    profile_res = await db.execute(select(Profile).where(Profile.id == current_user.id))
    profile = profile_res.scalar_one_or_none()
    stats_res = await db.execute(select(UserStatistics).where(UserStatistics.user_id == current_user.id))
    stats = stats_res.scalar_one_or_none()
    return {
        "id": str(current_user.id), "name": current_user.name, "email": current_user.email,
        "learning_level": profile.learning_level if profile else "beginner",
        "xp": profile.xp if profile else 0,
        "level": profile.level if profile else 1,
        "streak_days": profile.streak_days if profile else 0,
        "statistics": {"total_lessons": stats.total_lessons_completed if stats else 0, "total_circuits": stats.total_circuits_created if stats else 0, "total_quizzes": stats.total_quizzes_taken if stats else 0, "quiz_accuracy": round(stats.total_quiz_accuracy if stats else 0, 1)},
    }
'''

files["backend/app/api/v1/circuits.py"] = '''
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database.session import get_session
from app.models.circuit import Circuit
from app.models.user import UserStatistics
from app.schemas.circuit import CircuitCreate, CircuitUpdate, CircuitResponse
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
import uuid

router = APIRouter()

TEMPLATE_CIRCUITS = [
    {"template_name": "bell_state", "name": "Bell State", "qubits": 2, "classical_bits": 2, "circuit_data": {"operations": [{"gate": "H", "targets": [0], "controls": [], "column": 0}, {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1}, {"gate": "MEASURE", "targets": [0, 1], "controls": [], "column": 2}]}},
    {"template_name": "superposition", "name": "Superposition", "qubits": 1, "classical_bits": 1, "circuit_data": {"operations": [{"gate": "H", "targets": [0], "controls": [], "column": 0}, {"gate": "MEASURE", "targets": [0], "controls": [], "column": 1}]}},
    {"template_name": "ghz", "name": "GHZ State", "qubits": 3, "classical_bits": 3, "circuit_data": {"operations": [{"gate": "H", "targets": [0], "controls": [], "column": 0}, {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1}, {"gate": "CNOT", "targets": [2], "controls": [0], "column": 2}, {"gate": "MEASURE", "targets": [0, 1, 2], "controls": [], "column": 3}]}},
]

@router.get("/templates")
async def get_templates():
    return {"templates": TEMPLATE_CIRCUITS}

@router.post("", response_model=CircuitResponse, status_code=status.HTTP_201_CREATED)
async def create_circuit(data: CircuitCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    circuit = Circuit(user_id=current_user.id, **data.model_dump())
    db.add(circuit)
    stats_res = await db.execute(select(UserStatistics).where(UserStatistics.user_id == current_user.id))
    stats = stats_res.scalar_one_or_none()
    if stats:
        stats.total_circuits_created += 1
    await db.commit()
    await db.refresh(circuit)
    return circuit

@router.get("")
async def list_circuits(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).where(Circuit.user_id == current_user.id).order_by(desc(Circuit.updated_at)))
    return {"circuits": [CircuitResponse.model_validate(c) for c in result.scalars().all()]}

@router.get("/{circuit_id}", response_model=CircuitResponse)
async def get_circuit(circuit_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.user_id == current_user.id))
    circuit = result.scalar_one_or_none()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit

@router.put("/{circuit_id}", response_model=CircuitResponse)
async def update_circuit(circuit_id: uuid.UUID, data: CircuitUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.user_id == current_user.id))
    circuit = result.scalar_one_or_none()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(circuit, field, value)
    await db.commit()
    await db.refresh(circuit)
    return circuit

@router.delete("/{circuit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_circuit(circuit_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.user_id == current_user.id))
    circuit = result.scalar_one_or_none()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    await db.delete(circuit)
    await db.commit()
'''

files["backend/app/api/v1/simulation.py"] = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.schemas.simulation import SimulationRequest, StepRequest, SimulationResult, StepResult
from app.quantum.simulator import QuantumSimulator
from app.quantum.step_executor import StepExecutor
from app.models.circuit import SimulationHistory
from app.models.user import UserStatistics
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
import uuid

router = APIRouter()
simulator = QuantumSimulator()
step_executor = StepExecutor()

@router.post("/run")
async def run_simulation(request: SimulationRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = simulator.run(request.qubits, request.operations, request.shots)
    history = SimulationHistory(user_id=current_user.id, circuit_id=uuid.UUID(request.circuit_id) if request.circuit_id else None, input_data={"qubits": request.qubits, "operations": request.operations, "shots": request.shots}, result_data=result, execution_time_ms=int(result.get("execution_time", 0)), shots=request.shots)
    db.add(history)
    stats_res = await db.execute(select(UserStatistics).where(UserStatistics.user_id == current_user.id))
    stats = stats_res.scalar_one_or_none()
    if stats:
        stats.total_simulations_run += 1
    await db.commit()
    return result

@router.post("/step")
async def run_step(request: StepRequest, current_user: User = Depends(get_current_user)):
    return step_executor.execute_step(request.qubits, request.operations, request.step_index)

@router.get("/history")
async def get_history(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SimulationHistory).where(SimulationHistory.user_id == current_user.id).order_by(desc(SimulationHistory.created_at)).limit(20))
    history = result.scalars().all()
    return {"history": [{"id": str(h.id), "shots": h.shots, "execution_time_ms": h.execution_time_ms, "created_at": h.created_at.isoformat(), "result": h.result_data} for h in history]}
'''

files["backend/app/api/v1/algorithms.py"] = '''
from fastapi import APIRouter, HTTPException
from app.quantum.algorithms.grover import build_grover_circuit
from app.quantum.algorithms.teleportation import build_teleportation_circuit
from app.quantum.algorithms.deutsch_jozsa import build_deutsch_jozsa_circuit
from app.quantum.algorithms.qft import build_qft_circuit
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

ALGORITHMS = [
    {"slug": "grover", "name": "Grover\'s Search", "description": "Quadratic speedup for unstructured search", "complexity": "O(√N)", "icon": "search"},
    {"slug": "teleportation", "name": "Quantum Teleportation", "description": "Transfer quantum state using entanglement", "complexity": "3 qubits", "icon": "zap"},
    {"slug": "deutsch-jozsa", "name": "Deutsch-Jozsa", "description": "Determine if function is constant or balanced", "complexity": "O(1) queries", "icon": "function-square"},
    {"slug": "qft", "name": "Quantum Fourier Transform", "description": "Exponentially faster Fourier transform", "complexity": "O(n²)", "icon": "waves"},
]

class GroverRequest(BaseModel):
    n_qubits: int = 3
    target: int = 5
    iterations: Optional[int] = None

class TeleportRequest(BaseModel):
    state: str = "plus"

class DJRequest(BaseModel):
    oracle_type: str = "balanced"
    n_qubits: int = 3

class QFTRequest(BaseModel):
    n_qubits: int = 3
    input_state: int = 0

@router.get("")
async def list_algorithms():
    return {"algorithms": ALGORITHMS}

@router.post("/grover/run")
async def run_grover(req: GroverRequest):
    if req.n_qubits < 2 or req.n_qubits > 5:
        raise HTTPException(status_code=400, detail="n_qubits must be 2-5")
    return build_grover_circuit(req.n_qubits, req.target, req.iterations)

@router.post("/teleportation/run")
async def run_teleportation(req: TeleportRequest):
    return build_teleportation_circuit(req.state)

@router.post("/deutsch-jozsa/run")
async def run_deutsch_jozsa(req: DJRequest):
    return build_deutsch_jozsa_circuit(req.oracle_type, req.n_qubits)

@router.post("/qft/run")
async def run_qft(req: QFTRequest):
    if req.n_qubits < 1 or req.n_qubits > 6:
        raise HTTPException(status_code=400, detail="n_qubits must be 1-6")
    return build_qft_circuit(req.n_qubits, req.input_state)
'''

files["backend/app/api/v1/learning.py"] = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.learning import LearningModule, Lesson, LessonProgress, ProgressStatus
from app.models.user import UserStatistics
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from datetime import datetime
import uuid

router = APIRouter()

@router.get("/modules")
async def get_modules(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LearningModule).where(LearningModule.is_published == True).order_by(LearningModule.level, LearningModule.order_index))
    modules = result.scalars().all()
    return {"modules": [{"id": str(m.id), "title": m.title, "description": m.description, "level": m.level, "icon": m.icon, "lesson_count": len(m.lessons)} for m in modules]}

@router.get("/modules/{module_id}")
async def get_module(module_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LearningModule).where(LearningModule.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Module not found")
    return {"id": str(module.id), "title": module.title, "description": module.description, "level": module.level, "lessons": [{"id": str(l.id), "title": l.title, "order_index": l.order_index, "xp_reward": l.xp_reward, "estimated_minutes": l.estimated_minutes} for l in module.lessons]}

@router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"id": str(lesson.id), "title": lesson.title, "content": lesson.content, "xp_reward": lesson.xp_reward, "estimated_minutes": lesson.estimated_minutes}

@router.post("/progress")
async def update_progress(data: dict, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    lesson_id = uuid.UUID(data["lesson_id"])
    result = await db.execute(select(LessonProgress).where(LessonProgress.user_id == current_user.id, LessonProgress.lesson_id == lesson_id))
    progress = result.scalar_one_or_none()
    if not progress:
        progress = LessonProgress(user_id=current_user.id, lesson_id=lesson_id)
        db.add(progress)
    progress.status = ProgressStatus.completed
    progress.completed_at = datetime.utcnow()
    progress.time_spent_seconds = data.get("time_spent_seconds", 0)
    stats_res = await db.execute(select(UserStatistics).where(UserStatistics.user_id == current_user.id))
    stats = stats_res.scalar_one_or_none()
    if stats:
        stats.total_lessons_completed += 1
    await db.commit()
    return {"success": True, "xp_earned": 50}

@router.get("/progress")
async def get_progress(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LessonProgress).where(LessonProgress.user_id == current_user.id))
    progress = result.scalars().all()
    return {"completed": [str(p.lesson_id) for p in progress if p.status == ProgressStatus.completed], "in_progress": [str(p.lesson_id) for p in progress if p.status == ProgressStatus.in_progress]}
'''

files["backend/app/api/v1/ai_tutor.py"] = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.ai import ChatRequest, ChatResponse, ExplainCircuitRequest
from app.models.ai import AIConversation, AIMessage, MessageRole
from app.ai.provider import llm
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
import uuid

router = APIRouter()

@router.get("/conversations")
async def list_conversations(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AIConversation).where(AIConversation.user_id == current_user.id))
    convs = result.scalars().all()
    return {"conversations": [{"id": str(c.id), "title": c.title, "created_at": c.created_at.isoformat()} for c in convs]}

@router.post("/conversations/{conv_id}/chat", response_model=ChatResponse)
async def chat(conv_id: str, request: ChatRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    conv_uuid = uuid.UUID(conv_id)
    result = await db.execute(select(AIConversation).where(AIConversation.id == conv_uuid, AIConversation.user_id == current_user.id))
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msgs_res = await db.execute(select(AIMessage).where(AIMessage.conversation_id == conv_uuid))
    history = [{"role": m.role, "content": m.content} for m in msgs_res.scalars().all()]
    history.append({"role": "user", "content": request.message})
    response = await llm.chat(history, request.difficulty)
    user_msg = AIMessage(conversation_id=conv_uuid, role=MessageRole.user, content=request.message)
    ai_msg = AIMessage(conversation_id=conv_uuid, role=MessageRole.assistant, content=response)
    db.add(user_msg)
    db.add(ai_msg)
    await db.commit()
    return ChatResponse(response=response, conversation_id=conv_id)

@router.post("/conversations")
async def create_conversation(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    conv = AIConversation(user_id=current_user.id)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return {"id": str(conv.id), "title": conv.title}

@router.post("/explain-circuit")
async def explain_circuit(request: ExplainCircuitRequest, current_user: User = Depends(get_current_user)):
    return await llm.explain_circuit(request.circuit_data, request.difficulty)

@router.post("/generate-quiz")
async def generate_quiz(data: dict, current_user: User = Depends(get_current_user)):
    questions = await llm.generate_quiz(data.get("topic", "quantum computing"), data.get("difficulty", "beginner"), data.get("count", 5))
    return {"questions": questions}
'''

files["backend/app/api/v1/quiz.py"] = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.quiz import Quiz, Question, QuizAttempt, QuizAnswer
from app.models.user import UserStatistics, Profile
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from datetime import datetime
import uuid

router = APIRouter()

@router.get("/quizzes")
async def list_quizzes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quiz).where(Quiz.is_published == True))
    quizzes = result.scalars().all()
    return {"quizzes": [{"id": str(q.id), "title": q.title, "difficulty": q.difficulty, "xp_reward": q.xp_reward, "question_count": len(q.questions)} for q in quizzes]}

@router.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions = [{"id": str(q.id), "question_text": q.question_text, "question_type": q.question_type, "options": q.options} for q in quiz.questions]
    return {"id": str(quiz.id), "title": quiz.title, "difficulty": quiz.difficulty, "time_limit_seconds": quiz.time_limit_seconds, "xp_reward": quiz.xp_reward, "questions": questions}

@router.post("/quizzes/{quiz_id}/submit")
async def submit_quiz(quiz_id: uuid.UUID, submission: dict, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    answers = submission.get("answers", {})
    correct_count = 0
    answer_records = []
    for q in quiz.questions:
        user_ans = answers.get(str(q.id), "")
        is_correct = user_ans == q.correct_answer
        if is_correct:
            correct_count += 1
        answer_records.append({"question_id": q.id, "user_answer": user_ans, "is_correct": is_correct, "correct_answer": q.correct_answer, "explanation": q.explanation})
    total = len(quiz.questions)
    accuracy = round(correct_count / total * 100, 1) if total else 0
    xp_earned = quiz.xp_reward if accuracy == 100 else int(quiz.xp_reward * accuracy / 100)
    attempt = QuizAttempt(user_id=current_user.id, quiz_id=quiz_id, score=correct_count, accuracy=accuracy, time_taken_seconds=submission.get("time_taken", 0), xp_earned=xp_earned)
    db.add(attempt)
    await db.flush()
    for ar in answer_records:
        qa = QuizAnswer(attempt_id=attempt.id, question_id=ar["question_id"], user_answer=ar["user_answer"], is_correct=ar["is_correct"])
        db.add(qa)
    stats_res = await db.execute(select(UserStatistics).where(UserStatistics.user_id == current_user.id))
    stats = stats_res.scalar_one_or_none()
    if stats:
        stats.total_quizzes_taken += 1
        stats.total_quiz_accuracy = (stats.total_quiz_accuracy * (stats.total_quizzes_taken - 1) + accuracy) / stats.total_quizzes_taken
    profile_res = await db.execute(select(Profile).where(Profile.id == current_user.id))
    profile = profile_res.scalar_one_or_none()
    if profile:
        profile.xp += xp_earned
    await db.commit()
    return {"score": correct_count, "total": total, "accuracy": accuracy, "xp_earned": xp_earned, "answers": answer_records}
'''

files["backend/app/api/v1/achievements.py"] = '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.achievement import Achievement, UserAchievement
from app.core.dependencies import get_current_user, get_db
from app.models.user import User

router = APIRouter()

@router.get("")
async def list_achievements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Achievement).where(Achievement.is_hidden == False))
    achievements = result.scalars().all()
    return {"achievements": [{"id": str(a.id), "name": a.name, "description": a.description, "icon": a.icon, "badge_color": a.badge_color, "xp_reward": a.xp_reward} for a in achievements]}

@router.get("/user")
async def user_achievements(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserAchievement).where(UserAchievement.user_id == current_user.id))
    user_ach = result.scalars().all()
    return {"unlocked": [{"achievement_id": str(ua.achievement_id), "unlocked_at": ua.unlocked_at.isoformat()} for ua in user_ach]}
'''

# ─── TESTS ────────────────────────────────────────────────────────────────────
files["backend/tests/__init__.py"] = '# tests package\n'

files["backend/tests/test_quantum.py"] = '''
import pytest
from app.quantum.engine import CircuitBuilder
from app.quantum.simulator import QuantumSimulator
from app.quantum.step_executor import StepExecutor
from app.quantum.algorithms.grover import build_grover_circuit
from app.quantum.algorithms.deutsch_jozsa import build_deutsch_jozsa_circuit

@pytest.fixture
def simulator():
    return QuantumSimulator()

@pytest.fixture
def step_executor():
    return StepExecutor()

def test_hadamard_superposition(simulator):
    ops = [{"gate": "H", "targets": [0], "controls": [], "column": 0}]
    result = simulator.run(1, ops, shots=1024)
    assert result["success"]
    probs = result["probabilities"]
    assert abs(probs.get("0", 0) - 0.5) < 0.1
    assert abs(probs.get("1", 0) - 0.5) < 0.1

def test_bell_state(simulator):
    ops = [
        {"gate": "H", "targets": [0], "controls": [], "column": 0},
        {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1},
    ]
    result = simulator.run(2, ops, shots=1024)
    assert result["success"]
    probs = result["probabilities"]
    total = sum(v for k, v in probs.items() if k in {"00", "11"})
    assert total > 0.95  # Bell state: only 00 and 11

def test_x_gate(simulator):
    ops = [{"gate": "X", "targets": [0], "controls": [], "column": 0}]
    result = simulator.run(1, ops, shots=100)
    assert result["success"]
    assert result["probabilities"].get("1", 0) > 0.95

def test_step_executor(step_executor):
    ops = [
        {"gate": "H", "targets": [0], "controls": [], "column": 0},
        {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1},
    ]
    result = step_executor.execute_step(2, ops, 0)
    assert result["success"]
    assert result["gate_applied"] == "H"

def test_grover_finds_target():
    result = build_grover_circuit(3, 5)
    assert result["success"]
    target_key = format(5, "03b")
    assert result["probabilities"].get(target_key, 0) > 0.5

def test_deutsch_jozsa_constant():
    result = build_deutsch_jozsa_circuit("constant_zero", 3)
    assert result["success"]
    assert result["result"] == "constant"

def test_deutsch_jozsa_balanced():
    result = build_deutsch_jozsa_circuit("balanced", 3)
    assert result["success"]
    assert result["result"] == "balanced"
'''

files["backend/tests/test_api.py"] = '''
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"

@pytest.mark.asyncio
async def test_algorithms_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/algorithms")
    assert resp.status_code == 200
    assert "algorithms" in resp.json()

@pytest.mark.asyncio
async def test_circuit_templates():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/circuits/templates")
    assert resp.status_code == 200
'''

# ─── DATABASE SEED ────────────────────────────────────────────────────────────
files["backend/app/database/seed.py"] = '''
"""
Database seeder — populates learning modules, lessons, achievements, and quizzes.
Run: python -m app.database.seed
"""
import asyncio
from app.database.connection import engine, Base
from app.database.session import AsyncSessionLocal
from app.models.learning import LearningModule, Lesson
from app.models.achievement import Achievement
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
        {"title": "Grover\'s Search Algorithm", "xp_reward": 200, "estimated_minutes": 30},
        {"title": "Quantum Fourier Transform", "xp_reward": 200, "estimated_minutes": 30},
        {"title": "Shor\'s Algorithm (Overview)", "xp_reward": 250, "estimated_minutes": 35},
        {"title": "Quantum Teleportation", "xp_reward": 200, "estimated_minutes": 30},
        {"title": "Superdense Coding", "xp_reward": 150, "estimated_minutes": 25},
    ]},
]

ACHIEVEMENTS = [
    {"name": "Quantum Beginner", "description": "Complete your first lesson", "icon": "star", "badge_color": "blue", "unlock_condition": {"type": "lessons_completed", "value": 1}, "xp_reward": 50},
    {"name": "Gate Master", "description": "Complete all gate lessons", "icon": "cpu", "badge_color": "purple", "unlock_condition": {"type": "module_completed", "value": 2}, "xp_reward": 200},
    {"name": "Circuit Builder", "description": "Create 5 quantum circuits", "icon": "circuit-board", "badge_color": "cyan", "unlock_condition": {"type": "circuits_created", "value": 5}, "xp_reward": 150},
    {"name": "Entanglement Explorer", "description": "Run a Bell state simulation", "icon": "link", "badge_color": "pink", "unlock_condition": {"type": "simulations_run", "value": 1}, "xp_reward": 100},
    {"name": "Algorithm Expert", "description": "Explore all quantum algorithms", "icon": "zap", "badge_color": "gold", "unlock_condition": {"type": "algorithms_explored", "value": 4}, "xp_reward": 500},
    {"name": "Quantum Scientist", "description": "Reach 1000 XP", "icon": "flask", "badge_color": "green", "unlock_condition": {"type": "xp", "value": 1000}, "xp_reward": 250},
    {"name": "Quiz Champion", "description": "Score 100% on any quiz", "icon": "trophy", "badge_color": "gold", "unlock_condition": {"type": "perfect_quiz", "value": 1}, "xp_reward": 200},
    {"name": "Streak Master", "description": "7 day learning streak", "icon": "flame", "badge_color": "orange", "unlock_condition": {"type": "streak", "value": 7}, "xp_reward": 300},
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
        # Seed achievements
        for ach_data in ACHIEVEMENTS:
            session.add(Achievement(**ach_data))
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
'''

# ─── DOCKER / INFRA ───────────────────────────────────────────────────────────
files["docker-compose.yml"] = '''
version: "3.9"
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: quantumverse
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      db:
        condition: service_healthy

  frontend:
    build: ./frontend
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    env_file:
      - ./frontend/.env.local
    depends_on:
      - backend

volumes:
  pgdata:
'''

files["backend/Dockerfile"] = '''
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

# Write all files
for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content.lstrip('\n'))
    print(f"  wrote: {rel_path}")

print(f"\nTotal files written: {len(files)}")
