from datetime import datetime
from sqlalchemy import DateTime, Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=text("now()"),
        nullable=False
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(),
        onupdate=text("now()"),
        nullable=True
    )
