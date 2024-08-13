import cachetools
import uuid
import string

cache = cachetools.TTLCache(maxsize=100, ttl=300)


def generate_transfer_token(user_id: int):
    while True:
        token = str(uuid.uuid4())[:13]
        if token not in cache:
            break

    cache[token] = user_id
    return token


def validate_token(token: str) -> int:
    return cache.get(token) if token in cache else 0


def invalidate_token(token: str):
    cache.pop(token)
