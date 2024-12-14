from http import HTTPStatus

from fastapi import HTTPException

from app.schemas.auth import InviteChallenge
from app.schemas.user import UserOut
from app.services.base import BaseService, atomic
from app.models.user import User


class UserService(BaseService):
    """
    User model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "users"

    @atomic
    async def check_user_is_admin_in_org(
        self,
        user: User,
    ) -> bool:
        """
        Check if user is admin in organization.

        :param user: request user, for whom check is performed
        :return bool: True if user is admin in organization, else False.
        """
        return await self.uow.users.check_user_is_admin_in_org(user)

    @atomic
    async def generate_invite_for_new_employee(
        self,
        user: User,
        new_employee_account: str,
    ) -> InviteChallenge:
        """
        Generate invite for new employee.

        :param user: user which is generating invite.
        :param new_employee_account: account for generating invite.
        :return: an instance of InviteChallenge.
        """
        if await self.uow.companies.check_token_exists(new_employee_account):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Cannot generate invite for given email,"
                " as invite token for that email already exists",
            )
        if await self.uow.users.check_account_exists(new_employee_account):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Cannot generate invite for given email,"
                " as it's already taken, please choose another one",
            )
        if await self.check_user_is_admin_in_org(user):
            return await self.uow.companies.generate_invite_code(
                new_employee_account,
            )
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Only admin can invite new employees",
        )

    @atomic
    async def change_account(self, user: User, new_account: str) -> UserOut:
        """
        Change account for user.

        :param user: request user, for whom account will be changed.
        :param new_account: new account to which user's account will
         be changed.

        :return: instance of user.
        """
        if await self.uow.users.check_account_exists(new_account):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already taken",
            )
        return await self.uow.users.change_account(user, new_account)

    @atomic
    async def change_credentials(
        self,
        user: User,
        new_credentials: dict,
    ) -> UserOut:
        """
        Change name or surname for user.

        :param user: request user, for whom credentials will be changed.
        :param new_credentials: new credentials to which user's credentials
         will be changed.
        :return: instance of user.
        """
        return await self.uow.users.change_credentials(user, **new_credentials)

    @atomic
    async def get_self_info(self, user: User) -> UserOut:
        """
        Return information about current user.

        :param user: request user, whose information will be returned.
        :return: instance of user.
        """
        return UserOut.model_validate(user)
