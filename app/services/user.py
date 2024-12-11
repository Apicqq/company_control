from typing import Any, Optional
from http import HTTPStatus

from fastapi.exceptions import HTTPException

from app.models.user import User
from app.services.base import BaseService
from app.schemas.auth import AccessToken
from app.utils.auth import encode_jwt
from app.units_of_work.base import atomic


class UserService(BaseService):
    """
    User model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "users"
