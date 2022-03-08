from datetime import datetime, timedelta
from grdb.server.app.config import Config
import jwt


def assign_token(email: str, author_id: int) -> str:
    expiration = (datetime.now() + timedelta(hours=1)).timestamp()
    payload = {
        'email': email,
        'author_id': author_id,
        'expiration': expiration,
    }
    return jwt.encode(payload, Config.JWT_SECRET).decode('utf-8')


def parse_token(token: str) -> (str, float):
    payload = jwt.decode(token, Config.JWT_SECRET)
    return payload.get('email'), payload.get('author_id'), payload.get('expiration')


def is_valid(token: str) -> bool:
    payload = jwt.decode(token, Config.JWT_SECRET)
    expiration = payload.get('expiration')
    if expiration is None or is_expired(expiration):
        return False
    return True


def is_expired(expiration: float) -> bool:
    return expiration < datetime.now().timestamp()
