from pathlib import Path
import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expires_minutes: int = 15


class Settings(BaseSettings):
    """Settings used in the app."""

    postgres_db_url: str = (
        f"postgresql+asyncpg://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}"
        f":{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
    secret: str = "VERY_SECRET_SECRET"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    auth_jwt: AuthJWT = AuthJWT()

    # for test purposes
    MODE: str = "prod"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    TEST_DB_NAME: str = "test_db"


settings = Settings()
