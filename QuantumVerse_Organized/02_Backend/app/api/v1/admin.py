from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.circuit import Circuit
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    users_count = await db.scalar(select(func.count(User.id)))
    circuits_count = await db.scalar(select(func.count(Circuit.id)))

    return {
        "users": int(users_count or 0),
        "circuits": int(circuits_count or 0),
    }
