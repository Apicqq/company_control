from pydantic import BaseModel, EmailStr, ConfigDict


class CreateCompany(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str

class CompanyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company_name: str
