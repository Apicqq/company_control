from pydantic import BaseModel, EmailStr, ConfigDict


class ValidateEmail(BaseModel):
    account: EmailStr



class UserOut(BaseModel):
    model_config = ConfigDict(strict=True)
    id: int
    first_name: str
    last_name: str
    password: str
    account: EmailStr | None = None
    role: str
    is_active: bool = True


class UserLogin(BaseModel):
    account: EmailStr
    password: str
