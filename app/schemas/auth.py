from pydantic import BaseModel
from app.schemas.user import ValidateEmail


class InviteChallenge(BaseModel):
    account: ValidateEmail
    invite_token: str
