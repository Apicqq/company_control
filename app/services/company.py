from http import HTTPStatus
from typing import TypeVar

from fastapi.exceptions import HTTPException

from app.models.base import Base
from app.models.auth import InviteChallenge
from app.models.company import Company
from app.schemas.company import CompanyOut
from app.services.base import BaseService
from app.units_of_work.base import atomic


class CompanyService(BaseService):
    """
    Company model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "companies"

    @atomic
    async def get_company_by_email(self, account: str) -> bool:
        """
        Get company by email, to check if it exists.
        :param account: email of the company.
        :return bool: True if company exists, else False.
        """
        return await self.uow.companies.check_email_exists(account)

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
        Sign up company with given email and invite token.
        :param account: incoming email.
        :param invite_token: incoming invite token.
        :return: True if token-email pair is valid, False otherwise.
        """
        return await self.uow.companies.verify_invite(account, invite_token)

    @atomic
    async def create_company(self, **kwargs) -> CompanyOut:
        #TODO add uniqueness validation before executing queries
        """
        Create new company.
        :param kwargs:
        :return:
        """
        company: Company = await self.uow.companies.create_company(**kwargs)
        await self.uow.users.create_user(
            company_id=company.id,
            **kwargs
        )
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
        if await self.get_company_by_email(account):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already taken"
            )
        if await self.check_token_exists(account):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Invite token for that email already exists"
            )
        return await self.generate_invite_token(account)

    @atomic
    async def sign_up(self, body: dict[str, str]) -> dict[str, str]:
        """
        Sing up company with given email and invite token.
        :param body: email and invite token.
        :return: dictionary with status.
        """
        if await self.verify_invite(**body):
            return {"status": "OK"}
        raise HTTPException(
            status_code=400,
            detail="Either token or email is invalid"
        )
