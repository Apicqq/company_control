from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import select
from sqlalchemy_utils import Ltree

from app.models.company import Department
from app.repositories.base import SqlAlchemyRepository
from app.models.base import Base
from app.utils.exceptions import ParentNotFoundError

if TYPE_CHECKING:
    from sqlalchemy import Select

Model = TypeVar("Model", bound=Base)


class DepartmentRepository(SqlAlchemyRepository):
    """
    Repository class for Company model.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """

    async def create_department(self, department: Department) -> Department:
        """
        Create a department and return it.

        :param department: object of Department model.
        :return: object of Department model.
        """
        parent_path = None
        if department.parent_department:
            parent = await self.get_by_query_one_or_none(
                id=department.parent_department,
            )  # type: ignore[func-returns-value]
            if not parent:
                raise ParentNotFoundError(
                    "Parent department with specified id does not exist.",
                )
            parent_path = parent.path
        path = (
            f"{parent_path}.{department.name}"
            if parent_path
            else department.name
        )
        return await self.add_one_and_get_obj(
            name=department.name,
            path=Ltree(path),
            parent_department=department.parent_department,
            company_id=department.company_id,
        )

    async def get_all_sub_departments(
        self,
        department_id: int,
    ) -> Sequence[Department]:
        """
        Fetch all sub-departments of a given department by its ID.

        :param department_id: ID of the department.
        :return: List of sub-departments.
        """
        department = await self.get_by_query_one_or_none(
            id=department_id,
        )  # type: ignore[func-returns-value]
        if department:
            query: Select = select(Department).where(
                Department.path.descendant_of(department.path),
                Department.id != department.id,
            )
            result = await self.session.scalars(query)
            return result.all()
        return []
