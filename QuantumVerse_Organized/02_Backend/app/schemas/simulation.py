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
