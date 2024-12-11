from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.models.user import Role


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    account: EmailStr
    role: Role


class UserIn(UserOut):
    id: int
    password: str | bytes


class UserLoginForm(BaseModel):
    account: EmailStr = Field(..., validation_alias="username")
    password: str
