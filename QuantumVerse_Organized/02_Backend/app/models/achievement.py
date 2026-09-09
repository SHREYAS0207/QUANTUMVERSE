import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

class Achievement(Base):
    __tablename__ = "achievements"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    icon: Mapped[str] = mapped_column(String(100), default="trophy")
    badge_color: Mapped[str] = mapped_column(String(50), default="gold")
    unlock_condition: Mapped[dict] = mapped_column(JSON, default=dict)
    xp_reward: Mapped[int] = mapped_column(Integer, default=100)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    user_achievements: Mapped[list["UserAchievement"]] = relationship(back_populates="achievement")

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    achievement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("achievements.id"), nullable=False)
    unlocked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    achievement: Mapped["Achievement"] = relationship(back_populates="user_achievements")
