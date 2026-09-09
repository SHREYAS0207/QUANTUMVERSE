from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import Any
import uuid

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.circuit import Circuit

router = APIRouter(prefix="/circuits", tags=["circuits"])


class CircuitBody(BaseModel):
    name: str = "My Circuit"
    description: str | None = None
    qubits: int = 2
    classical_bits: int = 2
    circuit_data: dict[str, Any] = {}


@router.get("")
async def list_circuits(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(
        select(Circuit).where(Circuit.user_id == user.id, Circuit.is_template == False)
        .order_by(desc(Circuit.updated_at)).limit(50)
    )
    items = rows.scalars().all()
    return {"circuits": [_circuit_dict(c) for c in items]}


@router.post("", status_code=201)
async def create_circuit(body: CircuitBody, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = Circuit(
        user_id=user.id, name=body.name, description=body.description,
        qubits=body.qubits, classical_bits=body.classical_bits,
        circuit_data=body.circuit_data, is_template=False,
    )
    db.add(c)
    await db.commit()
    await db.refresh(c)

    # Update stats
    user.profile.total_circuits = (user.profile.total_circuits or 0) + 1
    await db.commit()

    return _circuit_dict(c)


@router.get("/templates")
async def list_templates(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(select(Circuit).where(Circuit.is_template == True))
    return {"templates": [_circuit_dict(c) for c in rows.scalars().all()]}


@router.get("/{circuit_id}")
async def get_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = await _get_or_404(db, circuit_id, user.id)
    return _circuit_dict(c)


@router.put("/{circuit_id}")
async def update_circuit(circuit_id: str, body: CircuitBody, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = await _get_or_404(db, circuit_id, user.id)
    c.name = body.name
    c.description = body.description
    c.qubits = body.qubits
    c.classical_bits = body.classical_bits
    c.circuit_data = body.circuit_data
    await db.commit()
    await db.refresh(c)
    return _circuit_dict(c)


@router.delete("/{circuit_id}", status_code=204)
async def delete_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    c = await _get_or_404(db, circuit_id, user.id)
    await db.delete(c)
    await db.commit()


async def _get_or_404(db: AsyncSession, circuit_id: str, user_id: uuid.UUID) -> Circuit:
    row = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.user_id == user_id))
    c = row.scalar_one_or_none()
    if not c:
        raise HTTPException(404, "Circuit not found")
    return c


def _circuit_dict(c: Circuit) -> dict:
    return {
        "id": str(c.id), "name": c.name, "description": c.description,
        "qubits": c.qubits, "classical_bits": c.classical_bits,
        "circuit_data": c.circuit_data, "is_template": c.is_template,
        "created_at": c.created_at.isoformat(), "updated_at": c.updated_at.isoformat(),
    }
