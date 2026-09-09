from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.learning import LearningModule, Lesson, LessonProgress

router = APIRouter(prefix="/learning", tags=["learning"])


@router.get("/modules")
async def list_modules(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(LearningModule).order_by(LearningModule.level, LearningModule.order_index))
    modules = rows.scalars().all()
    return {"modules": [{
        "id": str(m.id), "title": m.title, "description": m.description,
        "level": m.level, "icon": m.icon, "lesson_count": m.lesson_count,
    } for m in modules]}


@router.get("/modules/{module_id}")
async def get_module(module_id: str, db: AsyncSession = Depends(get_db)):
    row = await db.execute(select(LearningModule).where(LearningModule.id == module_id))
    module = row.scalar_one_or_none()
    if not module:
        raise HTTPException(404, "Module not found")
    rows = await db.execute(select(Lesson).where(Lesson.module_id == module_id).order_by(Lesson.order_index))
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
    row = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
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
    lesson = (await db.execute(select(Lesson).where(Lesson.id == lesson_id))).scalar_one_or_none()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    existing = await db.execute(
        select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson_id)
    )
    if not existing.scalar_one_or_none():
        prog = LessonProgress(user_id=user.id, lesson_id=lesson_id, completed=True)
        db.add(prog)
        user.xp = (user.xp or 0) + lesson.xp_reward
        user.level = max(1, user.xp // 500 + 1)
        if user.profile:
            user.profile.total_lessons = (user.profile.total_lessons or 0) + 1
        await db.commit()

    return {"xp_earned": lesson.xp_reward, "total_xp": user.xp}


@router.get("/progress")
async def get_progress(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    rows = await db.execute(
        select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.completed == True)
    )
    completed = [str(r.lesson_id) for r in rows.scalars().all()]
    return {"completed": completed, "in_progress": []}
