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
        stats = UserStatistics(
            total_lessons=getattr(profile, "total_lessons", 0) or 0,
            total_circuits=getattr(profile, "total_circuits", 0) or 0,
            total_quizzes=getattr(profile, "total_quizzes", 0) or 0,
            quiz_accuracy=getattr(profile, "quiz_accuracy", 0.0) or 0.0,
        ) if profile else UserStatistics()
        return cls(
            id=str(obj.id), name=obj.name, email=obj.email,
            learning_level=obj.learning_level or "beginner",
            xp=obj.xp or 0, level=obj.level or 1, streak_days=obj.streak_days or 0,
            statistics=stats,
        )
