from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr

class CreateCompany(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str

class CompanyOut(BaseModel):
    id: int
    account: EmailStr
    company_name: str
    first_name: str
    last_name: str

class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
