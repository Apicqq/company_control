from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import select, exists, insert
from jwt import InvalidTokenError

from app.repositories.base import SqlAlchemyRepository
from app.models.base import Base
from app.models.user import User
from app.utils.auth import encode_jwt, decode_jwt

if TYPE_CHECKING:
    from sqlalchemy import Select, Insert, Result

Model = TypeVar("Model", bound=Base)


class AuthRepository(SqlAlchemyRepository):
    """
    Repository class for authentication processes.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """

    @staticmethod
    async def issue_jwt(user: User) -> str:
        """
        Issue JWT token for given user.
        :return: encoded JWT-token.
        """
        jwt_payload = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "account": user.account
        }
        return encode_jwt(jwt_payload)

    @staticmethod
    async def decode_token(token: str) -> dict:
        try:
            decoded = decode_jwt(token)
        except InvalidTokenError:
            raise RuntimeError
        return decoded
