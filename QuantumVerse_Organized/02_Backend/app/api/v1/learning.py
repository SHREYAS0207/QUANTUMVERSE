from app.models.learning import (
    LearningModule,
    Lesson,
    LessonProgress,
    ProgressStatus,
)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User, UserStatistics

router = APIRouter(prefix="/learning", tags=["learning"])

@router.get("/modules")
async def list_modules(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(
        select(LearningModule).order_by(
            LearningModule.level,
            LearningModule.order_index
        )
    )
    modules = rows.scalars().all()

    result = []

    for m in modules:
        lesson_rows = await db.execute(
            select(Lesson).where(
                Lesson.module_id == m.id
            )
        )
        lesson_count = len(lesson_rows.scalars().all())

        result.append({
            "id": str(m.id),
            "title": m.title,
            "description": m.description,
            "level": m.level,
            "icon": m.icon,
            "lesson_count": lesson_count,
        })

    return {"modules": result}


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
            "youtube_url": l.youtube_url,
        } for l in lessons],
    }



@router.get("/lessons/{lesson_id}")
async def get_lesson(
    lesson_id: str,
    db: AsyncSession = Depends(get_db),
):
    row = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    lesson = row.scalar_one_or_none()

    if not lesson:
        raise HTTPException(404, "Lesson not found")

    return {
        "id": str(lesson.id),
        "title": lesson.title,
        "order_index": lesson.order_index,
        "xp_reward": lesson.xp_reward,
        "estimated_minutes": lesson.estimated_minutes,
        "content": lesson.content,
        "youtube_url": lesson.youtube_url,
    }


@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = (
        await db.execute(
            select(Lesson).where(Lesson.id == lesson_id)
        )
    ).scalar_one_or_none()

    if not lesson:
        raise HTTPException(404, "Lesson not found")

    existing = await db.execute(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id,
            LessonProgress.lesson_id == lesson_id,
        )
    )

    if existing.scalar_one_or_none():
        total_xp = user.profile.xp if user.profile else 0
        return {
            "xp_earned": 0,
            "total_xp": total_xp,
        }

    prog = LessonProgress(
        user_id=user.id,
        lesson_id=lesson_id,
        status=ProgressStatus.completed,
    )
    db.add(prog)

    if user.profile:
        user.profile.xp = (user.profile.xp or 0) + lesson.xp_reward
        user.profile.level = max(1, user.profile.xp // 500 + 1)

    statistics = (
        await db.execute(
            select(UserStatistics).where(
                UserStatistics.user_id == user.id
            )
        )
    ).scalar_one_or_none()

    if statistics:
        statistics.total_lessons_completed = (
            statistics.total_lessons_completed or 0
        ) + 1

    await db.commit()

    total_xp = user.profile.xp if user.profile else 0

    return {
        "xp_earned": lesson.xp_reward,
        "total_xp": total_xp,
    }


@router.get("/progress")
async def get_progress(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = await db.execute(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id
        )
    )

    progress_rows = rows.scalars().all()

    completed = [
        str(row.lesson_id)
        for row in progress_rows
        if row.status == ProgressStatus.completed
    ]

    in_progress = [
        str(row.lesson_id)
        for row in progress_rows
        if row.status == ProgressStatus.in_progress
    ]

    return {
        "completed": completed,
        "in_progress": in_progress,
    }
