from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Company(Base):
    """Database model for company."""

    company_name: Mapped[str] = mapped_column(String, unique=True)
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="company",
    )
