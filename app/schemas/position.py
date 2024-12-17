from pydantic import BaseModel, ConfigDict, Field


class PositionIn(BaseModel):
    """Schema for representation of a position in organization."""

    title: str = Field(..., min_length=1)
    department_id: int


class PositionOut(PositionIn):
    """
    Schema for representation of a position in organization.

    Used in responses.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    is_head_of_department: bool


class UserPosition(BaseModel):
    position: PositionOut
    user_id: int
    position_id: int
