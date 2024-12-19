from typing import Optional

from pydantic import BaseModel, ConfigDict


class DepartmentIn(BaseModel):
    """Schema for creating department."""

    name: str
    parent_department: Optional[int] = None
    company_id: int


class DepartmentOut(DepartmentIn):
    """Schema for department, used in responses."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    path: str
    head_id: Optional[int] = None


class DepartmentHead(BaseModel):
    """Schema for setting department head."""

    user_id: int
    department_id: int


class DepartmentUpdate(BaseModel):
    """Schema for updating department."""

    name: Optional[str] = None
