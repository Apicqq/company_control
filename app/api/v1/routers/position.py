from fastapi import APIRouter, Depends

from app.schemas.position import PositionOut, PositionIn, UserPosition
from app.services.position import PositionService

router = APIRouter(
    prefix="/positions",
)


@router.post(
    "/create",
    response_model=PositionOut
)
async def create_position(
        position: PositionIn,
        service: PositionService = Depends(PositionService),
):
    return await service.create_position(position)


@router.post(
    "/{position_id}/assign",
    response_model=UserPosition
)
async def assign_position(
        position_id: int,
        user_id: int,
        service: PositionService = Depends(PositionService),
):
    return await service.assign_position(position_id, user_id)

@router.get(
    "/{position_id}",
    response_model=PositionOut,
)
async def get_position(
        position_id: int,
        service: PositionService = Depends(PositionService),
):
    return await service.get_position(position_id)

@router.patch(
    "/{position_id}",
    response_model=PositionOut,
)
async def update_position(
        position_id: int,
        position: PositionIn,
        service: PositionService = Depends(PositionService),
):
    return await service.update_position(position_id, position)

@router.delete(
    "/{position_id}",
)
async def delete_position(
        position_id: int,
        service: PositionService = Depends(PositionService),
):
    return await service.delete_position(position_id)