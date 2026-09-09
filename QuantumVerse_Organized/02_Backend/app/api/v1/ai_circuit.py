"""AI-powered circuit generation from natural language."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.models.user import User
from app.ai.provider import get_ai_response

router = APIRouter(prefix="/ai-circuit", tags=["ai_circuit"])

CIRCUIT_TEMPLATES = {
    "bell": {
        "name": "Bell State",
        "qubits": 2, "classical_bits": 2,
        "operations": [
            {"gate": "H",    "targets": [0], "controls": [], "column": 0},
            {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1},
        ]
    },
    "ghz": {
        "name": "GHZ State",
        "qubits": 3, "classical_bits": 3,
        "operations": [
            {"gate": "H",    "targets": [0], "controls": [],  "column": 0},
            {"gate": "CNOT", "targets": [1], "controls": [0], "column": 1},
            {"gate": "CNOT", "targets": [2], "controls": [0], "column": 2},
        ]
    },
    "superposition": {
        "name": "Equal Superposition",
        "qubits": 2, "classical_bits": 2,
        "operations": [
            {"gate": "H", "targets": [0], "controls": [], "column": 0},
            {"gate": "H", "targets": [1], "controls": [], "column": 0},
        ]
    },
    "qft_2": {
        "name": "2-Qubit QFT",
        "qubits": 2, "classical_bits": 2,
        "operations": [
            {"gate": "H",  "targets": [0], "controls": [],  "column": 0},
            {"gate": "RZ", "targets": [1], "controls": [],  "column": 0, "params": {"angle": 1.5707963}},
            {"gate": "H",  "targets": [1], "controls": [],  "column": 1},
            {"gate": "SWAP","targets": [0,1], "controls": [], "column": 2},
        ]
    },
}

KEYWORDS = {
    "bell":          ["bell", "entangle", "maximize", "max entangl"],
    "ghz":           ["ghz", "3 qubit entangle", "three qubit"],
    "superposition": ["superpos", "both states", "hadamard"],
    "qft_2":         ["fourier", "qft"],
}


class GenerateRequest(BaseModel):
    description: str
    difficulty: str = "beginner"


@router.post("/generate")
async def generate_circuit(body: GenerateRequest, user: User = Depends(get_current_user)):
    desc_lower = body.description.lower()

    # First try keyword matching
    for key, words in KEYWORDS.items():
        if any(w in desc_lower for w in words):
            tpl = CIRCUIT_TEMPLATES[key].copy()
            tpl["source"] = "template"
            tpl["explanation"] = await get_ai_response(
                f"Explain briefly what a {tpl['name']} circuit does for a {body.difficulty} student.",
                [], body.difficulty
            )
            return tpl

    # Fall back to default with AI explanation
    tpl = CIRCUIT_TEMPLATES["bell"].copy()
    tpl["source"] = "fallback"
    tpl["explanation"] = (
        "I've loaded a Bell State circuit as a starting point. "
        "Describe something more specific like 'GHZ state', 'superposition', or 'QFT' for a custom circuit."
    )
    return tpl
