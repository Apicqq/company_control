from collections.abc import Sequence
from typing import Any

from app.units_of_work.base import atomic, UnitOfWork


class BaseService:
    """
    Basic service for performing standard operations with the base repository.

    params:
        - base_repository: string like AbstractUnitOfWork class params
    """

    base_repository: str

    def __init__(self) -> None:
        """Apply Unit of Work to service."""
        self.uow: UnitOfWork = UnitOfWork()

    @atomic
    async def add_one(self, **kwargs: Any) -> None:
        """Add a new record to the database through unit of work."""
        await getattr(self.uow, self.base_repository).add_one(**kwargs)

    @atomic
    async def add_one_and_get_id(self, **kwargs: Any) -> int | str:
        """
        Add a new record to the database through unit of work.

        After that, return it's id.
        """
        return await getattr(
            self.uow,
            self.base_repository,
        ).add_one_and_get_id(**kwargs)

    @atomic
    async def add_one_and_get_obj(self, **kwargs: Any) -> Any:
        """
        Add a new record to the database through unit of work.

        After that, return the object.
        """
        return await getattr(
            self.uow,
            self.base_repository,
        ).add_one_and_get_obj(**kwargs)

    @atomic
    async def get_by_query_one_or_none(self, **kwargs: Any) -> Any:
        """
        Get an object from the database via unit of work.

        After that, return the object (if found) or None.
        """
        return await getattr(
            self.uow,
            self.base_repository,
        ).get_by_query_one_or_none(**kwargs)

    @atomic
    async def get_by_query_all(self, **kwargs: Any) -> Sequence[Any]:
        """
        Get sequence of objects from the database via unit of work.

        After that, return them (if found).
        """
        return await getattr(self.uow, self.base_repository).get_by_query_all(
            **kwargs,
        )

    @atomic
    async def update_one_by_id(self, obj_id: int | str, **kwargs: Any) -> Any:
        """
        Update an object from the database via unit of work.

        After that, return it (if found).
        """
        return await getattr(self.uow, self.base_repository).update_one_by_id(
            obj_id,
            **kwargs,
        )

    @atomic
    async def delete_by_query(self, **kwargs: Any) -> None:
        """Delete an object from the database via unit of work."""
        await getattr(self.uow, self.base_repository).delete_by_query(**kwargs)

    @atomic
    async def delete_all(self) -> None:
        """Delete all objects from the database via unit of work."""
        await getattr(self.uow, self.base_repository).delete_all()
