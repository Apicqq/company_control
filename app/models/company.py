from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Ltree, LtreeType

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
    departments: Mapped[list["Department"]] = relationship(
        "Department",
        back_populates="company",
    )


class Department(Base):
    """Database model for departments with nested structure using ltree."""

    name: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[Ltree] = mapped_column(LtreeType)
    parent_department: Mapped[int] = mapped_column(
        Integer, ForeignKey("department.id"),
        nullable=True,
    )
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"))

    parent: Mapped["Department"] = relationship(
        "Department",
        back_populates="children",
        remote_side="Department.id",
    )
    children: Mapped[list["Department"]] = relationship(
        "Department",
        back_populates="parent",
    )
    positions: Mapped[list["Position"]] = relationship(
        "Position",
        back_populates="department",
    )
    company: Mapped[Company] = relationship(
        "Company", back_populates="departments"
    )


class Position(Base):
    """Database model for job positions."""

    title: Mapped[str] = mapped_column(String, nullable=False)
    department_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("department.id")
    )

    department: Mapped["Department"] = relationship(
        "Department", back_populates="positions"
    )
    employees: Mapped[list["User"]] = relationship(
        "UserPosition", back_populates="position"
    )


class UserPosition(Base):
    """Mapping table for employees and their positions."""

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    position_id: Mapped[int] = mapped_column(Integer,
                                             ForeignKey("position.id"))

    user: Mapped["User"] = relationship(
        "User", back_populates="user_positions"
    )
    position: Mapped["Position"] = relationship(
        "Position", back_populates="employees"
    )
