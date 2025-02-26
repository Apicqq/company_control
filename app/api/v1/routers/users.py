from fastapi import APIRouter, Depends

from app.schemas.auth import InviteChallenge
from app.schemas.user import UserOut, EmployeeAccount, UserCredentials
from app.services.user import UserService
from app.api.v1.routers.auth import auth_required_dep

router = APIRouter(
    prefix="/users",
    tags=["users | v1"],
)


@router.get(
    "/me",
    response_model=UserOut,
)
async def check_self_info(
    current_user: auth_required_dep,
    service: UserService = Depends(UserService),
) -> UserOut:
    return await service.get_self_info(current_user)


@router.post(
    "/invite",
    response_model=InviteChallenge,
)
async def generate_invite_for_new_employee(
    new_employee_email: EmployeeAccount,
    current_user: auth_required_dep,
    service: UserService = Depends(UserService),
) -> InviteChallenge:
    return await service.generate_invite_for_new_employee(
        current_user,
        new_employee_email.account,
    )


@router.patch(
    "/change-account",
    response_model=UserOut,
)
async def change_account(
    new_account: EmployeeAccount,
    current_user: auth_required_dep,
    service: UserService = Depends(UserService),
) -> UserOut:
    return await service.change_account(current_user, new_account.account)


@router.patch(
    "/change-credentials",
    response_model=UserOut,
)
async def change_credentials(
    new_credentials: UserCredentials,
    current_user: auth_required_dep,
    service: UserService = Depends(UserService),
) -> UserOut:
    return await service.change_credentials(
        current_user,
        new_credentials.model_dump(),
    )
