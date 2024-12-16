from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.company import Company


class Role(Enum):
    """Enum, which represents available user roles in company."""

    USER = "user"
    ADMIN = "admin"


class User(Base):
    """Database model for user."""

    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    account: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[Role] = mapped_column(default=Role.ADMIN)
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="users",
    )
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"))
    user_positions = relationship("UserPosition", back_populates="user")

