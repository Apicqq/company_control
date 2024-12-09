from typing import Any, Sequence, TypeVar, TYPE_CHECKING, Union, Optional, \
    Protocol

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

if TYPE_CHECKING:
    from sqlalchemy import Insert, Select, Update, Delete
    from sqlalchemy.engine import Result

Model = TypeVar("Model", bound=Base)


class AbstractRepository(Protocol):
    """
    Abstract Repository class.

    Implements all the CRUD operations for working with any database.
    """

    async def add_one(self, *args: Any, **kwargs: Any) -> None:
        """Create single object."""
        ...

    async def add_one_and_get_id(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Union[int, str]:
        """Create single object and return it's id."""
        ...

    async def add_one_and_get_obj(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> type[Model]:
        """Create single object and return it."""
        ...

    async def get_by_query_one_or_none(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[type[Model]]:
        """Get single object or None if not found."""
        ...

    async def get_by_query_all(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Sequence[Model]]:
        """Get sequence of objects or None if not found."""
        ...

    async def update_one_by_id(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[type[Model]]:
        """Update an object by it's id."""
        ...

    async def delete_by_query(self, *args: Any, **kwargs: Any) -> None:
        """Delete an object that meets the query."""
        ...

    async def delete_all(self, *args: Any, **kwargs: Any) -> None:
        """Delete all objects."""
        ...

class SqlAlchemyRepository:
    """
    Basic repository class.

    Implements all CRUD methods with base table using SQLAlchemy.

    params:
        - model: SQLAlchemy child DeclarativeBase class
    """

    def __init__(
        self,
        session: AsyncSession,
        model: type[Model],
    ) -> None:
        """Initialize the class."""
        self.session = session
        self.model = model

    async def add_one(self, *args: Any, **kwargs: Any) -> None:
        """Insert one object into the database."""
        query: Insert = insert(self.model).values(**kwargs)
        await self.session.execute(query)

    async def add_one_and_get_id(self, *args: Any, **kwargs: Any) -> int | str:
        """Add an object into the database and return it's ID."""
        query: Insert = (
            insert(self.model)
            .values(**kwargs)
            .returning(
                self.model.id,
            )
        )
        obj_id: Result = await self.session.execute(query)
        return obj_id.scalar_one()

    async def add_one_and_get_obj(self, **kwargs: Any) -> Model:
        """Add an object into the database and return it."""
        query: Insert = (
            insert(self.model)
            .values(**kwargs)
            .returning(
                self.model,
            )
        )
        obj: Result = await self.session.execute(query)
        return obj.scalar_one()

    async def get_by_query_one_or_none(self, **kwargs: Any) -> Model | None:
        """Get an object by query or None if not found."""
        query: Select = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_by_query_all(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Sequence[Model]]:
        """Get sequence of objects by query or None if not found."""
        query: Select = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.scalars().all()

    async def update_one_by_id(
        self,
        obj_id: int | str,
        **kwargs: Any,
    ) -> Optional[Model]:
        """Update an object by it's id."""
        query: Update = (
            update(self.model)
            .filter(
                self.model.id == obj_id,
            )
            .values(**kwargs)
            .returning(self.model)
        )
        obj: Result = await self.session.execute(query)
        return obj.scalar_one_or_none()

    async def delete_by_query(self, **kwargs: Any) -> None:
        """Delete an object that meets the query."""
        query: Delete = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)

    async def delete_all(self) -> None:
        """Delete all objects."""
        query: Delete = delete(self.model)
        await self.session.execute(query)
