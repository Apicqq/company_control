from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordBearer

from app.schemas.auth import AccessToken
from app.services.auth import AuthService
from app.schemas.user import UserIn, UserLoginForm, UserOut

router = APIRouter(
    prefix="/auth/jwt", tags=["JWT"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/jwt/login")


async def validate_auth_user(
        user_data: Annotated[UserLoginForm, Form()],
        service: AuthService = Depends(AuthService)
):
    return await service.validate_auth_user(**user_data.model_dump())


async def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
        service: AuthService = Depends(AuthService),
) -> dict:
    return await service.decode_token(token)


async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        service: AuthService = Depends(AuthService),
) -> UserOut:
    return await service.get_current_auth_user(payload)


@router.post("/login", response_model=AccessToken)
async def issue_jwt(
        user: UserIn = Depends(validate_auth_user),
        service: AuthService = Depends(AuthService)
):
    return await service.issue_jwt(user)
