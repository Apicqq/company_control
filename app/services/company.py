from http import HTTPStatus
from typing import TYPE_CHECKING

from fastapi.exceptions import HTTPException
from email_validator import validate_email, EmailNotValidError

from app.models.auth import InviteChallenge
from app.schemas.company import CompanyOut
from app.services.base import BaseService, atomic
# from app.units_of_work.base import atomic

if TYPE_CHECKING:
    from app.models.company import Company


class CompanyService(BaseService):
    """
    Company model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "companies"

    @atomic
    async def check_email_exists(self, account: str) -> bool:
        """
        Check whether email exists in database.

        :param account: email of the company.
        :return bool: True if email exists in database, else False.
        """
        return await self.uow.users.check_account_exists(account)

    @atomic
    async def generate_invite_token(self, account: str) -> InviteChallenge:
        """
        Generate invite token for company with given email.

        :param account: email of the company.
        :return: object of InviteChallenge model.
        """
        return await self.uow.companies.generate_invite_code(account)

    @atomic
    async def check_token_exists(self, account: str) -> bool:
        """
        Check if token was already created for given email.

        :param account: incoming email.
        :return: True if token exists, False otherwise.
        """
        return await self.uow.companies.check_token_exists(account)

    @atomic
    async def verify_invite(self, account: str, invite_token: str) -> bool:
        """
        Verify if token-email pair is valid.

        :param account: incoming email.
        :param invite_token: incoming invite token.
        :return: True if token-email pair is valid, False otherwise.
        """
        return await self.uow.companies.verify_invite(account, invite_token)

    @atomic
    async def create_company(self, **kwargs) -> CompanyOut:
        """
        Create new company.

        :param kwargs: data to create a company.
        :return: created company in CompanyOut schema.
        """
        company: Company = await self.uow.companies.create_company(**kwargs)
        await self.uow.users.create_user(company_id=company.id, **kwargs)
        return CompanyOut.model_validate(company)

    @atomic
    async def check_account(self, account: str) -> InviteChallenge:
        """
        Check if company with given email already exists.

        if not, but token has already been created, but not used yet,
        raise HTTPException.
        :param account: incoming email.
        :return: object of InviteChallenge model.
        """
        try:
            validate_email(account)
        except EmailNotValidError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email is not valid",
            )
        if await self.check_email_exists(account):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already taken",
            )
        if await self.check_token_exists(account):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Invite token for that email already exists",
            )
        return await self.generate_invite_token(account)

    @atomic
    async def sign_up(self, body: dict[str, str]) -> dict[str, str]:
        """
        Sign up company with given email and invite token.

        :param body: email and invite token.
        :return: dictionary with status.
        """
        if await self.verify_invite(**body):
            return {"status": "OK"}
        raise HTTPException(
            status_code=400,
            detail="Either token or email is invalid",
        )
