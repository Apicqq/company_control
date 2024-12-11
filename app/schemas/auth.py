from pydantic import BaseModel


class InviteChallenge(BaseModel):
    account: str
    invite_token: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"
