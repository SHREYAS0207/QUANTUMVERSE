import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.learning import LearningModule, Lesson, LessonProgress, ProgressStatus

router = APIRouter(prefix="/learning", tags=["learning"])


def _parse_uuid(value: str, field_name: str) -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise HTTPException(400, f"Invalid {field_name}") from exc


@router.get("/modules")
async def list_modules(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(LearningModule).order_by(LearningModule.level, LearningModule.order_index))
    modules = rows.scalars().all()
    lesson_counts = dict((await db.execute(
        select(Lesson.module_id, func.count(Lesson.id)).group_by(Lesson.module_id)
    )).all())
    return {"modules": [{
        "id": str(m.id), "title": m.title, "description": m.description,
        "level": m.level, "icon": m.icon, "lesson_count": lesson_counts.get(m.id, 0),
    } for m in modules]}


@router.get("/modules/{module_id}")
async def get_module(module_id: str, db: AsyncSession = Depends(get_db)):
    module_uuid = _parse_uuid(module_id, "module_id")
    row = await db.execute(select(LearningModule).where(LearningModule.id == module_uuid))
    module = row.scalar_one_or_none()
    if not module:
        raise HTTPException(404, "Module not found")
    rows = await db.execute(select(Lesson).where(Lesson.module_id == module_uuid).order_by(Lesson.order_index))
    lessons = rows.scalars().all()
    return {
        "id": str(module.id), "title": module.title, "description": module.description,
        "level": module.level, "lessons": [{
            "id": str(l.id), "title": l.title, "order_index": l.order_index,
            "xp_reward": l.xp_reward, "estimated_minutes": l.estimated_minutes,
        } for l in lessons],
    }


@router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: str, db: AsyncSession = Depends(get_db)):
    lesson_uuid = _parse_uuid(lesson_id, "lesson_id")
    row = await db.execute(select(Lesson).where(Lesson.id == lesson_uuid))
    lesson = row.scalar_one_or_none()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return {
        "id": str(lesson.id), "title": lesson.title, "content": lesson.content,
        "xp_reward": lesson.xp_reward, "estimated_minutes": lesson.estimated_minutes,
    }


@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    lesson_uuid = _parse_uuid(lesson_id, "lesson_id")
    lesson = (await db.execute(select(Lesson).where(Lesson.id == lesson_uuid))).scalar_one_or_none()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    existing = await db.execute(
        select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson_uuid)
    )
    progress = existing.scalar_one_or_none()
    if not progress:
        progress = LessonProgress(
            user_id=user.id,
            lesson_id=lesson_uuid,
            status=ProgressStatus.completed,
            completed_at=datetime.now(timezone.utc),
        )
        db.add(progress)
        if user.profile:
            user.profile.xp = (user.profile.xp or 0) + lesson.xp_reward
            user.profile.level = max(1, user.profile.xp // 500 + 1)
        if user.statistics:
            user.statistics.total_lessons_completed += 1
        await db.commit()

    return {"xp_earned": lesson.xp_reward, "total_xp": user.profile.xp if user.profile else 0}


@router.get("/progress")
async def get_progress(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id,
            LessonProgress.status == ProgressStatus.completed,
        )
    )
    completed = [str(r.lesson_id) for r in rows.scalars().all()]
    return {"completed": completed, "in_progress": []}
