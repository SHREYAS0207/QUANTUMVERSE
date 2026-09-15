import uuid
from datetime import datetime, date, timezone
from sqlalchemy import String, Integer, Float, Boolean, Enum, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base
import enum

class LearningLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    circuits: Mapped[list["Circuit"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    statistics: Mapped["UserStatistics"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    learning_level: Mapped[LearningLevel] = mapped_column(Enum(LearningLevel), default=LearningLevel.beginner)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    streak_days: Mapped[int] = mapped_column(Integer, default=0)
    last_active_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    user: Mapped["User"] = relationship(back_populates="profile")

class UserStatistics(Base):
    __tablename__ = "user_statistics"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    total_lessons_completed: Mapped[int] = mapped_column(Integer, default=0)
    total_circuits_created: Mapped[int] = mapped_column(Integer, default=0)
    total_simulations_run: Mapped[int] = mapped_column(Integer, default=0)
    total_quizzes_taken: Mapped[int] = mapped_column(Integer, default=0)
    total_quiz_accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    total_time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user: Mapped["User"] = relationship(back_populates="statistics")
