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
