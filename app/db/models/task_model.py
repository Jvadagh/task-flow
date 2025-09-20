from enum import Enum
from datetime import date
from sqlalchemy import (
    String,
    Enum as SaEnum,
    Column,
    Date,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class Status(Enum):
    open = "open"
    doing = "doing"
    close = "close"


class TaskModel(Base):
    __tablename__ = "tasks"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status: Mapped[str] = mapped_column(SaEnum(Status), nullable=False, server_default=Status.open.value)
    due_date: Mapped[date] = mapped_column(Date, nullable=True)
