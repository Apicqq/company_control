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
    async def get_company_by_email(self, email: str) -> Optional[Any]:
        """
        Get company by email, to check if it exists.
        :param email: email of the company.
        :return bool: True if company exists, else False.
        """
        return await self.uow.companies.get_company_by_email(email)

    @atomic
    async def generate_invite_token(self, email: str) -> None:
        """
        Generate invite token for company with given email.
        :param email:
        :return:
        """
        return await self.uow.companies.generate_invite_code(email)

    @atomic
    async def check_token_exists(self, email: str) -> bool:
        return await self.uow.companies.check_token_exists(email)