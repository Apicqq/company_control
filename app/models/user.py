from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.company import Company


class Role(Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped["Role"] = mapped_column(String, default=Role.ADMIN)
    company: Mapped["Company"] = relationship("Company",back_populates="users")
