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
