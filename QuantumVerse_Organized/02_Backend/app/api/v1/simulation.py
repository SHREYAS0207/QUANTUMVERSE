from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.circuit import SimulationHistory
from app.quantum.simulator import run_simulation
from app.quantum.step_executor import execute_step
from pydantic import BaseModel
from typing import Any

router = APIRouter(prefix="/simulation", tags=["simulation"])


class RunRequest(BaseModel):
    qubits: int = 2
    classical_bits: int = 2
    operations: list[dict[str, Any]] = []
    shots: int = 1024
    circuit_id: str | None = None


class StepRequest(BaseModel):
    qubits: int = 2
    operations: list[dict[str, Any]] = []
    step_index: int = 0


@router.post("/run")
async def run(body: RunRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = run_simulation(body.qubits, body.classical_bits, body.operations, body.shots)

    # Persist to history
    hist = SimulationHistory(
        user_id=user.id,
        circuit_id=body.circuit_id,
        shots=body.shots,
        result_data=result,
    )
    db.add(hist)
    await db.commit()

    return result


@router.post("/step")
async def step(body: StepRequest, user: User = Depends(get_current_user)):
    return execute_step(body.qubits, body.operations, body.step_index)


@router.get("/history")
async def history(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    from sqlalchemy import select, desc
    rows = await db.execute(
        select(SimulationHistory).where(SimulationHistory.user_id == user.id).order_by(desc(SimulationHistory.created_at)).limit(20)
    )
    items = rows.scalars().all()
    return {"history": [{
        "id": str(h.id),
        "circuit_id": str(h.circuit_id) if h.circuit_id else None,
        "shots": h.shots,
        "created_at": h.created_at.isoformat(),
        "result": h.result_data,
    } for h in items]}
