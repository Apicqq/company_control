from typing import Any, TYPE_CHECKING, TypeVar, Sequence, Optional

from sqlalchemy import select, exists, insert

from app.models.company import UserPosition, Department, Position
from app.repositories.base import SqlAlchemyRepository
from app.models.base import Base
from app.models.user import User

if TYPE_CHECKING:
    from sqlalchemy import Select, Insert, Result

Model = TypeVar("Model", bound=Base)


class PositionRepository(SqlAlchemyRepository):
    """
    Repository class for Company model.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """

    async def check_user_in_requested_company(
        self,
        user_id: int,
        position_id: int,
    ) -> bool:
        """Check if user is in specified organization."""
        query: Select = (
            select(User.id)
            .join(Position, Position.id == position_id)
            .join(Department, Position.department_id == Department.id)
            .where(
                User.id == user_id,
                User.company_id == Department.company_id,
            )
        )
        result: Result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user is not None

    async def check_position_has_employees(self, position_id: int) -> bool:
        """Check if position has employees."""
        query: Select = select(
            exists().where(UserPosition.position_id == position_id),
        )
        return await self.session.scalar(query)

    async def create_position(self, **kwargs: Any) -> Model:
        """Create new position for specified company."""
        return await self.add_one_and_get_obj(**kwargs)

    async def assign_position(self, **kwargs: Any) -> Model:
        """Assign position to employee."""
        query: Insert = (
            insert(UserPosition)
            .values(**kwargs)
            .returning(
                UserPosition,
            )
        )
        obj: Result = await self.session.execute(query)
        return obj.scalar_one()

    async def get_user_position(self, user_id: int) -> Sequence[Model]:
        """Fetch specified user position."""
        query: Select = select(UserPosition).where(
            UserPosition.user_id == user_id,
        )
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def get_position_by_id(self, position_id: int) -> Optional[Model]:
        """Get position by given position id from UserPosition table."""
        query: Select = (
            select(Position)
            .join(UserPosition, Position.id == UserPosition.position_id)
            .where(UserPosition.position_id == position_id)
        )
        result: Result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def check_user_has_requested_position(
        self,
        user_id: int,
        position_id: int,
    ) -> bool:
        """Check whether requested user is already assigned to position."""
        query: Select = select(
            exists()
            .where(UserPosition.user_id == user_id)
            .where(UserPosition.position_id == position_id),
        )
        return await self.session.scalar(query)

    async def update_position(
        self,
        position_id: int,
        **kwargs: Any,
    ) -> Optional[Model]:
        """Update position data for specified company."""
        return await self.update_one_by_id(position_id, **kwargs)

    async def delete_position(self, position_id: int) -> None:
        """Delete position for specified company."""
        await self.delete_by_query(id=position_id)
