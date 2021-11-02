from datetime import datetime, timedelta
import jwt
from ...config import Config


def assign_token(email: str) -> str:
    expiration = (datetime.now() + timedelta(hours=1)).timestamp()
    payload = {
        'email': email,
        'expiration': expiration
    }
    return jwt.encode(payload, Config.JWT_SECRET).decode('utf-8')


def is_expired(expiration: float) -> bool:
    return expiration < datetime.now().timestamp()
