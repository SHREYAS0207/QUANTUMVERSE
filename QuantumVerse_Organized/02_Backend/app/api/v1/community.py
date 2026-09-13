import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.circuit import Circuit, CircuitLike

router = APIRouter(prefix="/community", tags=["community"])


def _parse_uuid(value: str, field_name: str) -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise HTTPException(400, f"Invalid {field_name}") from exc


@router.get("/circuits")
async def list_public(db: AsyncSession = Depends(get_db), sort: str = "recent", limit: int = 20):
    """List publicly shared circuits."""
    query = select(Circuit).where(Circuit.is_public == True)
    if sort == "popular":
        query = query.order_by(desc(Circuit.like_count))
    else:
        query = query.order_by(desc(Circuit.created_at))
    rows = await db.execute(query.limit(limit))
    return {"circuits": [_public_dict(c) for c in rows.scalars().all()]}


@router.post("/circuits/{circuit_id}/like")
async def like_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    circuit_uuid = _parse_uuid(circuit_id, "circuit_id")
    c = await _get_public_or_404(db, circuit_uuid)
    existing = await db.execute(select(CircuitLike).where(CircuitLike.circuit_id == circuit_uuid, CircuitLike.user_id == user.id))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Already liked")
    db.add(CircuitLike(circuit_id=circuit_uuid, user_id=user.id))
    c.like_count = (c.like_count or 0) + 1
    await db.commit()
    return {"likes": c.like_count}


@router.delete("/circuits/{circuit_id}/like", status_code=204)
async def unlike_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    circuit_uuid = _parse_uuid(circuit_id, "circuit_id")
    existing = await db.execute(select(CircuitLike).where(CircuitLike.circuit_id == circuit_uuid, CircuitLike.user_id == user.id))
    like = existing.scalar_one_or_none()
    if not like:
        raise HTTPException(404, "Not liked")
    c = await _get_public_or_404(db, circuit_uuid)
    await db.delete(like)
    c.like_count = max(0, (c.like_count or 1) - 1)
    await db.commit()


@router.post("/circuits/{circuit_id}/publish")
async def publish_circuit(circuit_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    circuit_uuid = _parse_uuid(circuit_id, "circuit_id")
    c = await _get_owned_or_404(db, circuit_uuid, user.id)
    c.is_public = True
    await db.commit()
    return {"published": True, "id": str(c.id)}


async def _get_public_or_404(db: AsyncSession, circuit_id: uuid.UUID) -> Circuit:
    row = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.is_public == True))
    c = row.scalar_one_or_none()
    if not c:
        raise HTTPException(404, "Circuit not found")
    return c

async def _get_owned_or_404(db: AsyncSession, circuit_id: uuid.UUID, user_id) -> Circuit:
    row = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.user_id == user_id))
    c = row.scalar_one_or_none()
    if not c:
        raise HTTPException(404, "Circuit not found")
    return c

def _public_dict(c: Circuit) -> dict:
    return {
        "id": str(c.id), "name": c.name, "description": c.description,
        "qubits": c.qubits, "like_count": c.like_count or 0,
        "created_at": c.created_at.isoformat(),
    }
