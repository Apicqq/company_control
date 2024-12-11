from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.models.user import Role


class UserOut(BaseModel):
    """
    Schema for User.

    Used in response.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    account: EmailStr
    role: Role


class UserIn(UserOut):
    """
    Schema for User.

    Used in JWT authentication.
    """

    password: str | bytes


class UserLoginForm(BaseModel):
    """
    Schema for User.

    Also used in JWT authentication, but only when directly logging in
    via form.
    """

    account: EmailStr = Field(..., validation_alias="username")
    password: str


class EmployeeAccount(BaseModel):
    """
    Schema for new User account, also known as employee.

    This schema is only used when admin of a company generates
    invite for new employee.
    """
    account: EmailStr


class UserCredentials(BaseModel):
    """
    Schema for new User account.

    Used for changing user's credentials, such as first name or last name.
    """

    first_name: str
    last_name: str