from fastapi import APIRouter, Depends
from mypy.reachability import assert_will_always_fail

from app.schemas.auth import InviteChallenge
from app.schemas.user import UserIn, UserOut, EmployeeAccount, UserCredentials
from app.services.user import UserService
from app.api.v1.routers.auth import get_current_auth_user

router = APIRouter(
    prefix="/users", tags=["users | v1"]
)


@router.get(
    "/me",
    response_model=UserOut
)
async def check_self_info(
    current_user: UserIn = Depends(get_current_auth_user),
) -> UserOut:
    return UserOut.model_validate(current_user)


@router.post(
    "/invite",
    response_model=InviteChallenge
)
async def generate_invite_for_new_employee(
        new_employee_email: EmployeeAccount,
        current_user: UserIn = Depends(get_current_auth_user),
        service: UserService = Depends(UserService),
) -> InviteChallenge:
    return await service.generate_invite_for_new_employee(
        current_user, new_employee_email.account
    )

@router.patch(
    "/change-account",
    response_model=UserOut,
)
async def change_account(
        new_account: EmployeeAccount,
        current_user: UserIn = Depends(get_current_auth_user),
        service: UserService = Depends(UserService),
) -> UserOut:
    return await service.change_account(current_user, new_account.account)

@router.patch(
    "/change-credentials",
    response_model=UserOut
)
async def change_credentials(
        new_credentials: UserCredentials,
        current_user: UserIn = Depends(get_current_auth_user),
        service: UserService = Depends(UserService),
) -> UserOut:
    return await service.change_credentials(
        current_user, new_credentials.model_dump()
    )