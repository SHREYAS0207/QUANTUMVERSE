from fastapi import APIRouter
from pydantic import BaseModel

from app.quantum.algorithms.grover import run_grover
from app.quantum.algorithms.teleportation import run_teleportation
from app.quantum.algorithms.deutsch_jozsa import run_deutsch_jozsa
from app.quantum.algorithms.qft import run_qft

router = APIRouter(prefix="/algorithms", tags=["algorithms"])

ALGORITHMS_META = [
    {"id": "grover",          "name": "Grover's Search",           "complexity": "O(√N)",        "category": "search"},
    {"id": "teleportation",   "name": "Quantum Teleportation",      "complexity": "3 qubits",       "category": "communication"},
    {"id": "deutsch-jozsa",   "name": "Deutsch-Jozsa",             "complexity": "O(1) queries",   "category": "query"},
    {"id": "qft",             "name": "Quantum Fourier Transform",  "complexity": "O(n²)",        "category": "transform"},
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
