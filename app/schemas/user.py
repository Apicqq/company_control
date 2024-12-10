from pydantic import BaseModel, EmailStr, ConfigDict


class ValidateEmail(BaseModel):
    account: EmailStr



class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
