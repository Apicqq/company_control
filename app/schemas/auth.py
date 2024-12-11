from pydantic import BaseModel


class InviteChallenge(BaseModel):
    """Schema for invite challenge."""

    account: str
    invite_token: str


class AccessToken(BaseModel):
    """Schema for JWT token."""

    access_token: str
    token_type: str = "Bearer"
