from typing import TypeVar

from app.repositories.base import SqlAlchemyRepository
from app.models.base import Base
from app.utils.auth import hash_password

Model = TypeVar("Model", bound=Base)


class UserRepository(SqlAlchemyRepository):
    """
    Repository class for User model.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """

    async def create_user(self, **kwargs) -> Model:
        """
        Create a user and return it.
        :param kwargs: data to create user.
        :return: created user.
        """
        password: str | None = kwargs.get("password")
        if password is None:
            raise ValueError("Password is required")

        user_data: dict = dict(
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            account=kwargs.get("account"),
            password=hash_password(password).decode("utf-8"),
            company_id=kwargs.get("company_id"),
        )
        return await self.add_one_and_get_obj(**user_data)
