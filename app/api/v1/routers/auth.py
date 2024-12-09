from fastapi import APIRouter


router = APIRouter(
    prefix="/auth",
)


@router.get("/check_account{account}")
async def check_account():
    return {"current_email": "test@test.test"}


@router.post("/sign-up")
async def sign_up():
    return {"status": "OK"}


@router.post("/sign-up-complete")
async def complete_sign_up():
    return {"status": "OK"}