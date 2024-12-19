from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import select, update, func, cast, exists
from sqlalchemy_utils import Ltree, LtreeType
from app.models.company import Department
from app.repositories.base import SqlAlchemyRepository
from app.models.base import Base
from app.models.user import User
from app.utils.exceptions import ParentNotFoundError

if TYPE_CHECKING:
    from sqlalchemy import Select, ScalarResult, Result, Update

Model = TypeVar("Model", bound=Base)


class DepartmentRepository(SqlAlchemyRepository):
    """
    Repository class for Company model.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """

    async def generate_department_path(self, department: Department) -> Ltree:
        """Generate Ltree path for new department."""
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
            f"{parent_path}.{department.name.replace(" ", "_")}"
            if parent_path
            else department.name
        )
        return Ltree(path)

    async def create_department(self, department: Department) -> Department:
        """
        Create a department and return it.

        :param department: object of Department model.
        :return: object of Department model.
        """
        path = await self.generate_department_path(department)
        return await self.add_one_and_get_obj(
            name=department.name,
            path=path,
            parent_department=department.parent_department,
            company_id=department.company_id,
        )

    async def check_department_has_subdepartments(
        self,
        department: Department,
    ) -> bool:
        """Check whether department have any descendant departments."""
        query: Select = select(
            exists().where(
                Department.path.descendant_of(department.path),
                Department.path != department.path,
            ),
        )
        return await self.session.scalar(query)

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
            result: ScalarResult = await self.session.scalars(query)
            return result.all()
        return []

    async def check_user_in_requested_department(
        self,
        user_id: int,
        department_id: int,
    ) -> bool:
        """Check if user is in specified organization."""
        query: Select = (
            select(User.id)
            .join(Department, Department.id == department_id)
            .where(
                User.id == user_id,
                User.company_id == Department.company_id,
            )
        )
        return await self.session.scalar(query)

    async def check_department_has_head(self, department_id: int) -> bool:
        """Check if requested department has head."""
        query: Select = select(Department.head_id).where(
            Department.id == department_id,
        )
        result: Result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user is not None

    async def set_department_head(
        self,
        user_id: int,
        department_id: int,
    ) -> Model | None:
        """Set given user as head of department."""
        query = select(Department).where(Department.id == department_id)
        result = await self.session.execute(query)
        department = result.scalar_one_or_none()
        if department:
            return await self.update_one_by_id(department_id, head_id=user_id)
        return None

    async def update_department(self, department_id: int, **kwargs) -> Model:
        """Update specified department with new data."""
        department: Department | None = await self.get_by_query_one_or_none(
            id=department_id,
        )
        old_path: LtreeType = department.path # type: ignore
        new_path = None
        if department:
            new_name = kwargs.get("name", department.name)
            department.name = new_name
            new_path = await self.generate_department_path(department)
        if new_path:
            updated = await self.update_one_by_id(
                department_id,
                path=new_path,
                **kwargs,
            ) # type: ignore[func-returns-value]
        else:
            updated = await self.update_one_by_id(
                department_id, **kwargs,
            ) # type: ignore[func-returns-value]
        await self.update_descendent_paths(old_path, new_path)
        return updated # type: ignore[return-value]

    async def update_descendent_paths(
        self,
        old_path: LtreeType, # type: ignore[valid-type]
        new_path: LtreeType, # type: ignore[valid-type]
    ) -> None:
        """Update Ltree paths for descendant departments."""
        query: Update = (
            update(Department)
            .where(
                Department.path.descendant_of(old_path),
                Department.path != new_path,
            )
            .values(
                path=cast(
                    func.concat(
                        str(new_path),
                        ".",
                        func.subpath(
                            Department.path,
                            func.nlevel(cast(old_path, LtreeType)),
                        ),
                    ),
                    LtreeType,
                ),
            )
        )
        await self.session.execute(query)

    async def delete_department(self, department_id: int):
        """Delete department with specified id."""
        await self.delete_by_query(id=department_id)
