from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import select, exists, insert

from app.repositories.base import SqlAlchemyRepository
from app.models.base import Base
from app.models.user import User
from app.models.auth import InviteChallenge
from app.utils.auth import generate_invite_code

if TYPE_CHECKING:
    from sqlalchemy import Select, Insert, Result

Model = TypeVar("Model", bound=Base)


class CompanyRepository(SqlAlchemyRepository):
    """
    Repository class for Company model.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """

    async def get_company_by_email(self, email: str) -> bool:
        """
        Get company by email, to check if it exists.
        :return:
        """
        query: Select = select(exists().where(User.email == email))
        return await self.session.scalar(query)

    async def check_token_exists(self, email: str) -> bool:
        """
        Check if token exists for given email.
        :return:
        """
        query: Select = select(
            exists().where(InviteChallenge.account == email)
        )
        return await self.session.scalar(query)

    async def generate_invite_code(self, email: str) -> type[Base]:
        """
        Generate invitation code for given email.
        :param email: email of the company.
        :return:
        """
        query: Insert = insert(InviteChallenge).values(
            account=email,
            invite_token=generate_invite_code(),
        ).returning(InviteChallenge)
        obj: Result = await self.session.execute(query)
        return obj.scalar_one()

    async def verify_invite(self, email: str, invite_token: str) -> None:
        """
        Verify given data, proceed if valid.
        :param email:
        :param invite_token:
        :return:
        """
        query: Select = select(
            exists().where(InviteChallenge.account == email)
            .where(InviteChallenge.invite_token == invite_token)
        )
        return await self.session.scalar(query)
