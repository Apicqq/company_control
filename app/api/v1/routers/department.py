from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.schemas.department import (
    DepartmentOut,
    DepartmentIn,
    DepartmentHead,
    DepartmentUpdate,
)
from app.services.department import DepartmentService

router = APIRouter(
    prefix="/departments",
)


@router.post(
    "/create",
    response_model=DepartmentOut,
)
async def create_department(
        department: DepartmentIn,
        service: DepartmentService = Depends(DepartmentService),
):
    return await service.create_department(department)


@router.get(
    "/{department_id}/sub_departments",
    response_model=list[DepartmentOut],
)
async def get_all_sub_departments(
        department_id: int,
        service: DepartmentService = Depends(DepartmentService),
):
    return await service.get_all_sub_departments(department_id)


@router.post("{department_id}/set_head")
async def set_department_head(
        department_head: DepartmentHead,
        service: DepartmentService = Depends(DepartmentService),
) -> DepartmentOut:
    return await service.set_department_head(department_head)


@router.patch(
    "{department_id}",
    response_model=DepartmentOut
)
async def update_department(
        department_id: int,
        department_data: DepartmentUpdate,
        service: DepartmentService = Depends(DepartmentService),
):
    return await service.update_department(department_id, department_data)


@router.delete("{department_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_department(
        department_id: int,
        service: DepartmentService = Depends(DepartmentService),
):
    return await service.delete_department(department_id)
