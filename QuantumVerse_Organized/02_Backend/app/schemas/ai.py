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
