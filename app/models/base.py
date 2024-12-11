from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base, declared_attr


class PreBase:
    """Base class for all models used by SQLAlchemy."""

    @declared_attr
    def __tablename__(cls):
        """Create table name from class name."""
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


Base = declarative_base(
    cls=PreBase,
    metadata=MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_"
            "%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
    ),
)
