from fastapi import APIRouter, Depends

from app.schemas.department import DepartmentOut, DepartmentIn
from app.services.department import DepartmentService


router = APIRouter(
    prefix="/departments",
)


@router.post(
    "/create",
    response_model=DepartmentOut
)
async def create_department(
        department: DepartmentIn,
        service: DepartmentService = Depends(DepartmentService),

):
    return await service.create_department(department)


@router.get(
    "/{department_id}/sub_departments",
    response_model=list[DepartmentOut]
)
async def get_all_sub_departments(
        department_id: int,
        service: DepartmentService = Depends(DepartmentService),

):
    return await service.get_all_sub_departments(department_id)
