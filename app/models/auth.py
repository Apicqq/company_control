from app.models.base import Base

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class InviteChallenge(Base):
    """Database model for invite challenge."""

    account: Mapped[str] = mapped_column(String)
    invite_token: Mapped[str] = mapped_column(String)
