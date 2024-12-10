from pydantic import BaseModel


class InviteChallenge(BaseModel):
    account: str
    invite_token: str
