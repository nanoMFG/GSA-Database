from datetime import datetime, timedelta
from server.config import Config
import jwt


def assign_token(email: str) -> str:
    expiration = (datetime.now() + timedelta(hours=1)).timestamp()
    payload = {
        'email': email,
        'expiration': expiration
    }
    return jwt.encode(payload, Config.JWT_SECRET).decode('utf-8')


def parse_token(token: str) -> (str, float):
    payload = jwt.decode(token, Config.JWT_SECRET)
    return payload.get('email'), payload.get('expiration')


def is_valid(token: str) -> bool:
    payload = jwt.decode(token, Config.JWT_SECRET)
    expiration = payload.get('expiration')
    if expiration is None or is_expired(expiration):
        return False
    return True


def is_expired(expiration: float) -> bool:
    return expiration < datetime.now().timestamp()
