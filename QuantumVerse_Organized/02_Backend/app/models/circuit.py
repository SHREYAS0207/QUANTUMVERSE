import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

class Circuit(Base):
    __tablename__ = "circuits"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    qubits: Mapped[int] = mapped_column(Integer, default=1)
    classical_bits: Mapped[int] = mapped_column(Integer, default=0)
    circuit_data: Mapped[dict] = mapped_column(JSON, default=dict)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False)
    template_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    like_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user: Mapped["User"] = relationship(back_populates="circuits")
    simulations: Mapped[list["SimulationHistory"]] = relationship(
        back_populates="circuit",
        cascade="all, delete-orphan",
    )
    likes: Mapped[list["CircuitLike"]] = relationship(
        back_populates="circuit",
        cascade="all, delete-orphan",
    )

class CircuitLike(Base):
    __tablename__ = "circuit_likes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    circuit_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("circuits.id"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    circuit: Mapped["Circuit"] = relationship(back_populates="likes")
    user: Mapped["User"] = relationship()


class SimulationHistory(Base):
    __tablename__ = "simulation_history"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    circuit_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("circuits.id"), nullable=True)
    input_data: Mapped[dict] = mapped_column(JSON, default=dict)
    result_data: Mapped[dict] = mapped_column(JSON, default=dict)
    execution_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    shots: Mapped[int] = mapped_column(Integer, default=1024)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    circuit: Mapped["Circuit | None"] = relationship(back_populates="simulations")
