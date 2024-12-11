from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import select, exists, insert

from app.repositories.base import SqlAlchemyRepository
from app.models.base import Base
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

    async def check_token_exists(self, email: str) -> bool:
        """
        Check if token exists for given email.

        :param email: incoming email.
        :return: True if such pair of token and email exists in database,
         False otherwise.
        """
        query: Select = select(
            exists().where(InviteChallenge.account == email),
        )
        return await self.session.scalar(query)

    async def generate_invite_code(self, account: str) -> InviteChallenge:
        """
        Generate invitation code for given email.

        :param account: email of the user.
        :return: object of InviteChallenge model.
        """
        query: Insert = (
            insert(InviteChallenge)
            .values(
                account=account,
                invite_token=generate_invite_code(),
            )
            .returning(InviteChallenge)
        )
        obj: Result = await self.session.execute(query)
        return obj.scalar_one()

    async def verify_invite(self, account: str, invite_token: str) -> bool:
        """
        Verify given data, proceed if valid.

        :param account: email of the user.
        :param invite_token: invite token of the user.
        :return: True if valid, False otherwise.
        """
        query: Select = select(
            exists()
            .where(InviteChallenge.account == account)
            .where(InviteChallenge.invite_token == invite_token),
        )
        return await self.session.scalar(query)

    async def create_company(self, **kwargs) -> Model:
        """
        Create a company and return it.

        :param kwargs: data to create a company.
        :return: object of Company model.
        """
        company_data = dict(
            company_name=kwargs.get("company_name"),
        )
        return await self.add_one_and_get_obj(**company_data)
