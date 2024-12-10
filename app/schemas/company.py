from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict

from app.schemas.user import UserOut

class CreateCompany(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str

class CompanyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    account: str
    company_name: str
    user: UserOut
