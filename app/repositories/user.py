from datetime import date
from typing import Any, Sequence, TYPE_CHECKING

from sqlalchemy import select, distinct, between


from app.repositories.base import SqlAlchemyRepository

if TYPE_CHECKING:
    from sqlalchemy import Result, Select


class UserRepository(SqlAlchemyRepository):
    """
    Repository class for User model.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """