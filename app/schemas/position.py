from typing import Annotated

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


class PositionUpdate(BaseModel):
    """
    Schema for representation of a position in organization.

    Used in update requests, so that all fields are not required.
    """

    title: Annotated[str | None, Field(min_length=1)]
    department_id: Annotated[int | None, Field(ge=1)]


class UserPositionIn(BaseModel):
    """Schema for assigning employee to a position."""

    position_id: int
    user_id: int


class UserPositionOut(BaseModel):
    """Schema for representing employee's position."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    position: PositionOut
