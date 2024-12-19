from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.schemas.position import (
    PositionOut,
    PositionIn,
    UserPositionIn,
    UserPositionOut,
    PositionUpdate,
)
from app.services.position import PositionService
from app.api.v1.routers.auth import auth_required_dep

router = APIRouter(
    prefix="/positions",
)


@router.post(
    "/create",
    response_model=PositionOut,
)
async def create_position(
    current_user: auth_required_dep,
    position: PositionIn,
    service: PositionService = Depends(PositionService),
):
    return await service.create_position(position)


@router.post(
    "/{position_id}/assign",
    response_model=UserPositionOut,
)
async def assign_position(
    current_user: auth_required_dep,
    assignee: UserPositionIn,
    service: PositionService = Depends(PositionService),
):
    return await service.assign_position(assignee)


@router.get(
    "/{position_id}",
    response_model=PositionOut,
)
async def get_position(
    current_user: auth_required_dep,
    position_id: int,
    service: PositionService = Depends(PositionService),
):
    return await service.get_position(position_id)


@router.patch(
    "/{position_id}",
    response_model=PositionOut,
)
async def update_position(
    current_user: auth_required_dep,
    position_id: int,
    position_data: PositionUpdate,
    service: PositionService = Depends(PositionService),
):
    return await service.update_position(position_id, position_data)


@router.delete(
    "/{position_id}",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_position(
    current_user: auth_required_dep,
    position_id: int,
    service: PositionService = Depends(PositionService),
):
    return await service.delete_position(position_id)
