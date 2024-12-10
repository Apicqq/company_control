from typing import Any, Optional
from http import HTTPStatus

from fastapi.exceptions import HTTPException

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
        return await self.uow.companies.get_company_by_email(account)

    @atomic
    async def generate_invite_token(self, account: str):
        """
        Generate invite token for company with given email.
        :param account: email of the company.
        :return:
        """
        return await self.uow.companies.generate_invite_code(account)

    @atomic
    async def check_token_exists(self, account: str) -> bool:
        """
        Check if token exists for given email.
        :param account:
        :return:
        """
        return await self.uow.companies.check_token_exists(account)

    @atomic
    async def verify_invite(self, account: str, invite_token: str):
        """
        Sign up company with given email and invite token.
        :param account: email of the company.
        :param invite_token: invite token of the company.
        :return:
        """
        return await self.uow.companies.verify_invite(account, invite_token)

    @atomic
    async def create_company(self, **kwargs):
        """
        Create new company.
        :param kwargs:
        :return:
        """
        return await self.uow.companies.create_company(**kwargs)
