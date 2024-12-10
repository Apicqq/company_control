from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import ValidateEmail
from app.schemas.auth import InviteChallenge
from app.schemas.company import CreateCompany, CompanyOut
from app.services.base import BaseService
from app.services.company import CompanyService

router = APIRouter(
    prefix="/auth",
)


@router.get(
    "/check_account/{account}",
    response_model=InviteChallenge,
)
async def check_account(
        account: str,
        service: CompanyService = Depends(CompanyService)
) -> InviteChallenge:
    if await service.get_company_by_email(account):
        raise HTTPException(status_code=400, detail="Email already taken")
    if await service.check_token_exists(account):
        raise HTTPException(
            status_code=400,
            detail="Invite token for that email already exists"
        )
    return await service.generate_invite_token(account)


@router.post("/sign-up", response_model=dict[str, str])
async def sign_up(
        body: InviteChallenge,
        service: CompanyService = Depends(CompanyService),
):
    if await service.verify_invite(**body.model_dump()):
        return {"status": "OK"}
    raise HTTPException(
        status_code=400,
        detail="Either token or email is invalid"
    )


@router.post(
    "/sign-up-complete",
    response_model=CreateCompany,
)
async def complete_sign_up(
        body: CreateCompany,
        service: CompanyService = Depends(CompanyService),
) -> CreateCompany:
    return await service.create_company(**body.model_dump())
