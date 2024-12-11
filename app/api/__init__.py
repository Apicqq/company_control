import asyncio

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routers import users, company, auth
from app.database.db import get_async_session

router = APIRouter()

router.include_router(
    users.router,
    prefix="/v1",
    tags=["auth | v1"],
)

router.include_router(company.router, prefix="/v1", tags=["auth | v1"])

router.include_router(auth.router, prefix="/v1", tags=["auth | v1"])

@router.get(
    path="/healthz/",
    tags=["healthz"],
    status_code=HTTP_200_OK,
)
async def health_check(
    session: AsyncSession = Depends(get_async_session),
):
    """Check api external connection."""

    async def check_service(service: str) -> None:
        try:
            if service == "postgres":
                await session.execute(text("SELECT 1"))
        except Exception:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    await asyncio.gather(
        *[
            check_service("postgres"),
        ],
    )

    return {"status": "OK"}
