from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.achievement import Achievement, UserAchievement

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("")
async def list_achievements(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Achievement).order_by(Achievement.xp_reward))
    return {"achievements": [{
        "id": str(a.id), "name": a.name, "description": a.description,
        "badge_icon": a.badge_icon, "badge_color": a.badge_color, "xp_reward": a.xp_reward,
    } for a in rows.scalars().all()]}


@router.get("/user")
async def user_achievements(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(select(UserAchievement).where(UserAchievement.user_id == user.id))
    return {"unlocked": [{
        "achievement_id": str(ua.achievement_id),
        "unlocked_at": ua.unlocked_at.isoformat(),
    } for ua in rows.scalars().all()]}
