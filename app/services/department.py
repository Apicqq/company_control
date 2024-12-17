from http import HTTPStatus

from fastapi.exceptions import HTTPException

from app.models.company import Department
from app.schemas.department import DepartmentOut
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
            ),
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
    async def update_department(self):
        """Update department data for specified company."""

    @atomic
    async def delete_department(self):
        """Delete department for specified company."""
