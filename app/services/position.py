from typing import Any
from http import HTTPStatus

from fastapi.exceptions import HTTPException

from app.schemas.position import PositionIn, PositionOut
from app.services.base import BaseService, atomic
from app.utils.exceptions import ParentNotFoundException


class PositionService(BaseService):
    """
    Company model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "positions"

    @atomic
    async def create_position(self, position: PositionIn) -> PositionOut:
        """Create new position for specified company."""
        return await self.uow.positions.create_position(position.model_dump())

    @atomic
    async def update_position(self):
        """Update position data for specified company."""

    @atomic
    async def delete_position(self):
        """Delete position for specified company."""

    @atomic
    async def assign_position(self):
        """Assign position to employee."""
