import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.quiz import Quiz, Question, QuizAttempt

router = APIRouter(prefix="/quiz", tags=["quiz"])


def _parse_uuid(value: str, field_name: str) -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise HTTPException(400, f"Invalid {field_name}") from exc


@router.get("/quizzes")
async def list_quizzes(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Quiz))
    quizzes = rows.scalars().all()
    question_counts = dict((await db.execute(
        select(Question.quiz_id, func.count(Question.id)).group_by(Question.quiz_id)
    )).all())
    return {"quizzes": [{
        "id": str(q.id), "title": q.title,
        "difficulty": q.difficulty, "xp_reward": q.xp_reward,
        "question_count": question_counts.get(q.id, 0),
    } for q in quizzes]}


@router.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id: str, db: AsyncSession = Depends(get_db)):
    quiz_uuid = _parse_uuid(quiz_id, "quiz_id")
    row = await db.execute(select(Quiz).where(Quiz.id == quiz_uuid))
    quiz = row.scalar_one_or_none()
    if not quiz:
        raise HTTPException(404, "Quiz not found")
    rows = await db.execute(select(Question).where(Question.quiz_id == quiz_uuid).order_by(Question.id))
    questions = rows.scalars().all()
    return {
        "id": str(quiz.id), "title": quiz.title, "difficulty": quiz.difficulty,
        "xp_reward": quiz.xp_reward, "time_limit_seconds": quiz.time_limit_seconds,
        "questions": [{
            "id": str(q.id), "question_text": q.question_text,
            "question_type": q.question_type,
            "options": q.options or [],
            "correct_answer": q.correct_answer,  # include for client-side validation
        } for q in questions],
    }


class SubmitBody(BaseModel):
    answers: dict[str, str]
    time_taken: int = 0


@router.post("/quizzes/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: str, body: SubmitBody,
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    quiz_uuid = _parse_uuid(quiz_id, "quiz_id")
    quiz = (await db.execute(select(Quiz).where(Quiz.id == quiz_uuid))).scalar_one_or_none()
    if not quiz:
        raise HTTPException(404, "Quiz not found")

    rows = await db.execute(select(Question).where(Question.quiz_id == quiz_uuid))
    questions = rows.scalars().all()

    correct = 0
    answer_results = []
    for q in questions:
        user_ans = body.answers.get(str(q.id), "")
        is_correct = user_ans == q.correct_answer
        if is_correct:
            correct += 1
        answer_results.append({
            "question_id": str(q.id),
            "user_answer": user_ans,
            "is_correct": is_correct,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation or "",
        })

    total = len(questions)
    accuracy = round(correct / total * 100) if total else 0
    xp_earned = round(quiz.xp_reward * accuracy / 100)

    attempt = QuizAttempt(
        user_id=user.id, quiz_id=quiz_uuid,
        score=correct, total_questions=total,
        time_taken=body.time_taken, xp_earned=xp_earned,
    )
    db.add(attempt)

    user.xp = (user.xp or 0) + xp_earned
    user.level = max(1, user.xp // 500 + 1)
    if user.profile:
        user.profile.total_quizzes = (user.profile.total_quizzes or 0) + 1
        prev_acc = user.profile.quiz_accuracy or 0
        count = user.profile.total_quizzes
        user.profile.quiz_accuracy = round((prev_acc * (count - 1) + accuracy) / count, 1)

    await db.commit()

    return {
        "score": correct, "total": total, "accuracy": accuracy,
        "xp_earned": xp_earned, "answers": answer_results,
    }
