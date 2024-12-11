from typing import Any, TYPE_CHECKING, TypeVar

from sqlalchemy import select, exists

from app.repositories.base import SqlAlchemyRepository
from app.models.base import Base
from app.models.user import User, Role
from app.utils.auth import hash_password

Model = TypeVar("Model", bound=Base)

if TYPE_CHECKING:
    from sqlalchemy import Select


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

    async def check_account_exists(self, email: str) -> bool:
        """
        Get User by email, to check if it exists.

        :param email: incoming email.
        :return: True if such email exists in database, False otherwise.
        """
        query: Select = select(exists().where(User.account == email))
        return await self.session.scalar(query)

    async def check_user_is_admin_in_org(self, user: User) -> bool:
        """
        Check if user is admin in organization.

        :param user: incoming user.
        :return: True if user is admin, False otherwise.
        """
        query: Select = select(
            exists().where(User.id == user.id).where(User.role == Role.ADMIN),
        )
        return await self.session.scalar(query)

    async def change_account(self, user: User, new_account: str) -> User:
        """
        Change account for user.

        :param user: incoming user.
        :param new_account: new account to which user's account will
         be changed.
        :return: an instance of User.
        """
        return await self.update_one_by_id(user.id, account=new_account)

    async def change_credentials(self, user: User, **kwargs: Any) -> User:
        """
        Change credentials for user.

        :param user: incoming user.
        :param kwargs: new credentials to which user's credentials will
         be changed.

        :return: an instance of User.
        """
        return await self.update_one_by_id(user.id, **kwargs)
