from http import HTTPStatus

from fastapi.exceptions import HTTPException

from app.models.company import Department
from app.schemas.department import (
    DepartmentOut,
    DepartmentHead,
    DepartmentUpdate,
)
from app.services.base import BaseService, atomic
from app.utils.exceptions import ParentNotFoundError


class DepartmentService(BaseService):
    """
    Company model-specific service.

    Used for performing actions with repository.
    """

    base_repository: str = "departments"

    @classmethod
    def validate_incoming_department(
        cls,
        department: DepartmentOut,
    ) -> DepartmentOut:
        """
        Validate incoming department data.

        This is a workaround method to pass data through pydantic validation,
        so that it won't fail to coerce Ltree path field to string.
        """
        return DepartmentOut.model_validate(
            dict(
                id=department.id,
                path=str(department.path),
                name=department.name,
                parent_department=department.parent_department,
                company_id=department.company_id,
                head_id=department.head_id,
            ),
        )

    @atomic
    async def check_user_in_requested_department(
        self,
        user_id: int,
        department_id: int,
    ) -> bool:
        """Check that user is in requested department."""
        return await self.uow.departments.check_user_in_requested_department(
            user_id,
            department_id,
        )

    @atomic
    async def check_department_has_head(self, department_id: int) -> bool:
        """Check if requested department has head."""
        return await self.uow.departments.check_department_has_head(
            department_id,
        )

    @atomic
    async def check_department_has_subdepartments(
        self,
        department: Department,
    ) -> bool:
        """Check whether a department has any sub-departments linked to it."""
        return await self.uow.departments.check_department_has_subdepartments(
            department,
        )

    @atomic
    async def create_department(
        self,
        department: Department,
    ) -> DepartmentOut:
        """Create new department for specified company."""
        try:
            department = await self.uow.departments.create_department(
                department,
            )
            return self.validate_incoming_department(department)
        except ParentNotFoundError as exception:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=str(exception),
            )

    @atomic
    async def get_all_sub_departments(
        self,
        department_id: int,
    ) -> list[DepartmentOut]:
        """Get all sub-departments of a department for specified company."""
        departments = await self.uow.departments.get_all_sub_departments(
            department_id,
        )
        return [
            self.validate_incoming_department(department)
            for department in departments
        ]

    @atomic
    async def set_department_head(self, head: DepartmentHead) -> DepartmentOut:
        """Set head of a department."""
        if await self.check_department_has_head(head.department_id):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Department already has head",
            )
        if not await self.check_user_in_requested_department(
            head.user_id,
            head.department_id,
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Cannot set user as head of department,"
                "as requested user is not in specified department",
            )
        updated: DepartmentOut = (
            await self.uow.departments.set_department_head(**head.model_dump())
        )
        return self.validate_incoming_department(updated)

    @atomic
    async def update_department(
        self,
        department_id: int,
        department_data: DepartmentUpdate,
    ) -> DepartmentOut:
        """Update department data for specified company."""
        new_department = await self.uow.departments.update_department(
            department_id,
            **department_data.model_dump(exclude_unset=True),
        )
        return self.validate_incoming_department(new_department)

    @atomic
    async def delete_department(self, department_id: int) -> None:
        """Delete department for specified company."""
        if not (
            department := await self.get_by_query_one_or_none(id=department_id)
        ):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Department not found",
            )
        if await self.check_department_has_subdepartments(department):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Cannot delete department, as it has "
                "child sub-departments attached to it. "
                "Please move or delete them before proceeding.",
            )
        await self.uow.departments.delete_department(department_id)
