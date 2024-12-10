from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import ValidateEmail
from app.services.base import BaseService
from app.services.company import CompanyService

router = APIRouter(
    prefix="/auth",
)


@router.get(
    "/check_account{account}",
    response_model=dict[str, str],
)
async def check_account(
        account: str,
        service: CompanyService = Depends(CompanyService)
) -> dict[str, str]:
    if await service.get_company_by_email(account):
        raise HTTPException(status_code=400, detail="Email already taken")
    return {"OK": "True"}



@router.post("/sign-up")
async def sign_up(
        account: ValidateEmail,
        invite_token: str,
        service: CompanyService = Depends(CompanyService),
):
    return {"status": "OK"}


@router.post("/sign-up-complete")
async def complete_sign_up():
    return {"status": "OK"}
