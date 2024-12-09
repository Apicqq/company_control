from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
)


@router.get("/me")
async def read_users_me():
    return {"user_id": "the current user"}