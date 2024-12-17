from http import HTTPStatus
from typing import Optional, TYPE_CHECKING

from fastapi.exceptions import HTTPException

from app.schemas.position import (
    PositionIn,
    PositionOut,
    UserPositionIn,
    UserPositionOut,
    PositionUpdate,
)
from app.services.base import BaseService, atomic


if TYPE_CHECKING:
    from app.models.company import UserPosition


class PositionService(BaseService):
    """
    Company model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "positions"

    @atomic
    async def check_user_in_requested_company(
        self,
        user_id: int,
        position_id: int,
    ):
        """Check if user is in requested company."""
        return await self.uow.positions.check_user_in_requested_company(
            user_id,
            position_id,
        )

    @atomic
    async def check_user_has_requested_position(
        self,
        user_id: int,
        position_id: int,
    ) -> bool:
        """Check whether requested user is already assigned to position."""
        return await self.uow.positions.check_user_has_requested_position(
            user_id,
            position_id,
        )

    @atomic
    async def check_position_has_assigned_users(
        self,
        position_id: int,
    ) -> bool:
        """Check whether position has assigned users."""
        return await self.uow.positions.check_position_has_employees(
            position_id,
        )

    @atomic
    async def create_position(self, position: PositionIn) -> PositionOut:
        """Create new position for specified company."""
        return await self.uow.positions.create_position(
            **position.model_dump(),
        )

    @atomic
    async def assign_position(
        self,
        assignee: UserPositionIn,
    ) -> UserPositionOut | dict:
        """Assign position to employee."""
        if not await self.check_user_in_requested_company(
            assignee.user_id,
            assignee.position_id,
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Cannot assign employee to desired position, "
                "as employee is not in requested company",
            )
        if await self.check_user_has_requested_position(
            assignee.user_id,
            assignee.position_id,
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Requested user is already assigned "
                "to specified position.",
            )
        position = await self.uow.positions.get_position_by_id(
            assignee.position_id,
        )  # type: ignore[func-returns-value]
        if position:
            user_position: UserPosition = (
                await self.uow.positions.assign_position(
                    **assignee.model_dump(),
                )
            )
            return UserPositionOut(
                position=position,
                user_id=assignee.user_id,
                id=user_position.id,
            )
        return {"detail": "Position not found"}

    @atomic
    async def get_position(self, position_id: int) -> Optional[PositionOut]:
        """Get position by given position id."""
        return await self.uow.positions.get_position_by_id(
            position_id,
        )

    @atomic
    async def update_position(
        self,
        position_id: int,
        position_data: PositionUpdate,
    ) -> PositionOut | None:
        """Update position data for specified company."""
        return await self.uow.positions.update_position(
            position_id, **position_data.model_dump(exclude_unset=True)
        )

    @atomic
    async def delete_position(self, position_id: int) -> None:
        """Delete position for specified company."""
        if not self.get_position(position_id):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Position not found",
            )
        if await self.check_position_has_assigned_users(position_id):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Cannot delete position with assigned users",
            )
        await self.uow.positions.delete_position(position_id)
