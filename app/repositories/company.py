from typing import TYPE_CHECKING

from sqlalchemy import select, exists

from app.repositories.base import SqlAlchemyRepository
from app.models.user import User

if TYPE_CHECKING:
    from sqlalchemy import Select


class CompanyRepository(SqlAlchemyRepository):
    """
    Repository class for Company model.

    It uses SQLAlchemy as engine, and includes all base CRUD methods,
    as well as specific ones listed below.
    """

    async def get_company_by_email(self, email: str) -> bool:
        """
        Get company by email, to check if it exists.
        :return:
        """
        query: Select = select(exists().where(User.email == email))
        return await self.session.scalar(query)
