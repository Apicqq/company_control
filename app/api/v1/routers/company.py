from fastapi import APIRouter, Depends

from app.schemas.auth import InviteChallenge
from app.schemas.company import CreateCompany, CompanyOut
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
    service: CompanyService = Depends(CompanyService),
) -> InviteChallenge:
    return await service.check_account(account)


@router.post("/sign-up", response_model=dict[str, str])
async def sign_up(
    body: InviteChallenge,
    service: CompanyService = Depends(CompanyService),
):
    return await service.sign_up(body.model_dump())


@router.post(
    "/sign-up-complete",
    response_model=CompanyOut,
)
async def complete_sign_up(
    body: CreateCompany,
    company_service: CompanyService = Depends(CompanyService),
) -> CompanyOut:
    return await company_service.create_company(**body.model_dump())
