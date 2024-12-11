import datetime
from secrets import token_hex

import bcrypt
import jwt

from app.core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text("utf-8"),
    algorithm=settings.auth_jwt.algorithm,
    expires_in: int = settings.auth_jwt.access_token_expires_minutes,
) -> str:
    """
    Encode incoming payload to JWT token.
    :param payload: incoming payload, in dictionary format.
    :param private_key: private key to encode token.
    :param algorithm: algorithm to encode token.
    :param expires_in: token expiration time in minutes.
    :return: encoded JWT token.
    """
    now = datetime.datetime.now(datetime.UTC)
    to_encode = payload.copy()
    expire = now + datetime.timedelta(minutes=expires_in)
    to_encode.update(exp=expire, iat=now)
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text("utf-8"),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """
    Decode JWT token into dictionary format.
    :param token: encoded JWT token.
    :param public_key: public key to decode token.
    :param algorithm: algorithm to decode token.
    :return: decoded JWT token in dictionary format.
    """
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    """
    Hash incoming password.
    :param password: plain password to hash.
    :return: hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    """
    Verify if incoming password is correct to hashed one.
    :param password: plain password.
    :param hashed_password: hashed password.
    :return: True if passwords are equal, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


def generate_invite_code(n_bytes: int = 25) -> str:
    """
    Generate random invite code.
    :param n_bytes: number of bytes to generate string from.
    :return: randomly generated token string.
    """
    return token_hex(n_bytes)
