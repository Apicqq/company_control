from app.models.base import Base

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class InviteChallenge(Base):
    """Database model for invite challenge."""

    __table_args__ = (
        UniqueConstraint(
            "account", "invite_token", name="invite_token_unique"
        ),
    )

    account: Mapped[str] = mapped_column(String)
    invite_token: Mapped[str] = mapped_column(String)
