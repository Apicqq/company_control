from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.models.user import Role


class UserOut(BaseModel):
    """
    Schema for User.

    Used in response.
    """

    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    account: EmailStr
    role: Role


class UserIn(UserOut):
    """
    Schema for User.

    Used in JWT authentication.
    """

    id: int
    password: str | bytes


class UserLoginForm(BaseModel):
    """
    Schema for User.

    Also used in JWT authentication, but only when directly logging in
    via form.
    """

    account: EmailStr = Field(..., validation_alias="username")
    password: str
