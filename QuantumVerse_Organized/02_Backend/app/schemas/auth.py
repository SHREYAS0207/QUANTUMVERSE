from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    learning_level: Literal["beginner", "intermediate", "advanced"] = "beginner"

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("name")
    @classmethod
    def check_name(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    email: str
    learning_level: str


class UserStatistics(BaseModel):
    total_lessons: int = 0
    total_circuits: int = 0
    total_quizzes: int = 0
    quiz_accuracy: float = 0.0

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    learning_level: str
    xp: int
    level: int
    streak_days: int
    statistics: UserStatistics

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        profile = getattr(obj, "profile", None)
        learning_level = "beginner"
        xp = 0
        level = 1
        streak_days = 0

        if profile is not None:
            learning_level = getattr(profile, "learning_level", None)
            if hasattr(learning_level, "value"):
                learning_level = learning_level.value
            elif not learning_level:
                learning_level = "beginner"
            xp = getattr(profile, "xp", 0) or 0
            level = getattr(profile, "level", 0) or 1
            streak_days = getattr(profile, "streak_days", 0) or 0
        else:
            learning_level = getattr(obj, "learning_level", None) or "beginner"
            xp = getattr(obj, "xp", 0) or 0
            level = getattr(obj, "level", 0) or 1
            streak_days = getattr(obj, "streak_days", 0) or 0

        stats = UserStatistics(
            total_lessons=getattr(getattr(obj, "statistics", None), "total_lessons_completed", 0) or 0,
            total_circuits=getattr(getattr(obj, "statistics", None), "total_circuits_created", 0) or 0,
            total_quizzes=getattr(getattr(obj, "statistics", None), "total_quizzes_taken", 0) or 0,
            quiz_accuracy=getattr(getattr(obj, "statistics", None), "total_quiz_accuracy", 0.0) or 0.0,
        )
        return cls(
            id=str(obj.id), name=obj.name, email=obj.email,
            learning_level=learning_level,
            xp=xp,
            level=level,
            streak_days=streak_days,
            statistics=stats,
        )
