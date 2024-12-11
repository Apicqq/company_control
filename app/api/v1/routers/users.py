from fastapi import APIRouter, Depends

from app.schemas.user import UserIn, UserOut
from app.api.v1.routers.auth import get_current_auth_user

router = APIRouter(
    prefix="/users",
)


@router.get("/me")
async def check_self_info(
    current_user: UserIn = Depends(get_current_auth_user),
) -> UserOut:
    return UserOut.model_validate(current_user)


@router.post("/change-password")
async def change_password():
    pass
