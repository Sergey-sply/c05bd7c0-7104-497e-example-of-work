from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import DateTime



class Base(DeclarativeBase):
    __abstract__ = True

    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
