import datetime
from secrets import token_hex

import bcrypt
import jwt

from app.core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(
            "utf-8"
        ),
        algorithm=settings.auth_jwt.algorithm,
        expires_in: int = settings.auth_jwt.access_token_expires_minutes,
):
    now = datetime.datetime.now(datetime.UTC)
    to_encode = payload.copy()
    expire = now + datetime.timedelta(minutes=expires_in)
    to_encode.update(exp=expire, iat=now)
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text("utf-8"),
        algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


def generate_invite_code(n_bytes: int = 25):
    return token_hex(n_bytes)
