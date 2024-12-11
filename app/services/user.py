from app.services.base import BaseService


class UserService(BaseService):
    """
    User model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "users"
