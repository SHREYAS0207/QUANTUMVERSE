from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Any

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User, UserStatistics
from app.models.quiz import Quiz, Question, QuizAttempt

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/quizzes")
async def list_quizzes(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Quiz))
    quizzes = rows.scalars().all()

    result = []
    for q in quizzes:
        question_rows = await db.execute(
            select(Question.id).where(Question.quiz_id == q.id)
        )
        question_count = len(question_rows.scalars().all())

        result.append({
            "id": str(q.id),
            "title": q.title,
            "difficulty": q.difficulty,
            "xp_reward": q.xp_reward,
            "question_count": question_count,
        })

    return {"quizzes": result}


@router.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id: str, db: AsyncSession = Depends(get_db)):
    row = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = row.scalar_one_or_none()
    if not quiz:
        raise HTTPException(404, "Quiz not found")
    rows = await db.execute(select(Question).where(Question.quiz_id == quiz_id))
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
    quiz = (await db.execute(select(Quiz).where(Quiz.id == quiz_id))).scalar_one_or_none()
    if not quiz:
        raise HTTPException(404, "Quiz not found")

    rows = await db.execute(select(Question).where(Question.quiz_id == quiz_id))
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
        user_id=user.id,
        quiz_id=quiz.id,
        score=correct,
        accuracy=accuracy,
        time_taken_seconds=body.time_taken,
        xp_earned=xp_earned,
    )
    db.add(attempt)

    if user.profile:
        user.profile.xp = (user.profile.xp or 0) + xp_earned
        user.profile.level = max(1, user.profile.xp // 500 + 1)

    stats_row = await db.execute(
        select(UserStatistics).where(UserStatistics.user_id == user.id)
    )
    stats = stats_row.scalar_one_or_none()

    if not stats:
        stats = UserStatistics(user_id=user.id)
        db.add(stats)

    previous_attempts = stats.total_quizzes_taken or 0
    previous_accuracy = stats.total_quiz_accuracy or 0.0
    stats.total_quizzes_taken = previous_attempts + 1
    stats.total_quiz_accuracy = round(
        (previous_accuracy * previous_attempts + accuracy)
        / stats.total_quizzes_taken,
        1,
    )

    await db.commit()

    return {
        "score": correct, "total": total, "accuracy": accuracy,
        "xp_earned": xp_earned, "answers": answer_results,
    }
