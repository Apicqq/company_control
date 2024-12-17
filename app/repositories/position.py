from typing import Any, TYPE_CHECKING, TypeVar

from sqlalchemy import select, exists, insert

from app.repositories.base import SqlAlchemyRepository
from app.models.base import Base
from app.models.auth import InviteChallenge
from app.utils.auth import generate_invite_code

if TYPE_CHECKING:
    from sqlalchemy import Select, Insert, Result

Model = TypeVar("Model", bound=Base)


class PositionRepository(SqlAlchemyRepository):
    """
    Repository class for Company model.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """

    async def create_position(self, **kwargs: Any) -> Model:
        """Create new position for specified company."""
        return await self.add_one_and_get_obj(**kwargs)


    async def assign_position(self):
        """Assign position to employee."""


    async def get_user_position(self):
        """Fetch specified user position."""
        