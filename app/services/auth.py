from typing import Any, Optional
from http import HTTPStatus

from fastapi.exceptions import HTTPException

from app.models.user import User
from app.services.base import BaseService
from app.schemas.auth import AccessToken
from app.schemas.user import UserOut
from app.utils.auth import encode_jwt, verify_password
from app.units_of_work.base import atomic


class AuthService(BaseService):
    """
    User model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "auth"

    @atomic
    async def validate_auth_user(self, account: str, password: str) -> User:
        """
        Validate incoming pair of credentials, check if they are correct.
        :param account: email of the user.
        :param password: password of the user.
        :return: User object if credentials are valid.
        :raises HTTPException: if credentials are invalid.
        """
        invalid_user_exception = HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Invalid username or password",
        )
        if not (user := await self.get_by_query_one_or_none(account=account)):
            raise invalid_user_exception
        if not verify_password(
                password,
                bytes(user.password, encoding="utf-8")
        ):
            raise invalid_user_exception
        return user

    @atomic
    async def issue_jwt(self, user: User) -> AccessToken:
        """
        Issue JWT token for given user.
        :param user: User, for whom token is issued.
        :return: encoded JWT-token.
        """
        token = await self.uow.auth.issue_jwt(user)
        return AccessToken(access_token=token)

    @atomic
    async def decode_token(self, token: str) -> dict:
        """
        Decode JWT token into string.
        :param token: incoming token.
        :return: decoded token in dictionary format.
        """
        try:
            payload = await self.uow.auth.decode_token(token)
        except RuntimeError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return payload

    @atomic
    async def get_current_auth_user(
            self,
            payload: dict
    ) -> UserOut:
        """
        Try to get current user from token.
        :param payload: token payload.
        :return: current user.
        """
        user_account: str | None = payload.get("account")
        if not (
                user := await self.uow.auth.get_by_query_one_or_none(
                    # type: ignore[func-returns-value]
                    account=user_account
                )
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token data",
            )
        return UserOut.model_validate(user)
