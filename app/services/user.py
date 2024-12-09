from typing import Any, Optional
from http import HTTPStatus

from fastapi.exceptions import HTTPException

from app.services.base import BaseService
from app.units_of_work.base import atomic


class UserService(BaseService):
    """
    Instrument model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "instruments"
