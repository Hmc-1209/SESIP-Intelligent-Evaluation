import cachetools
import uuid
import string

cache = cachetools.TTLCache(maxsize=100, ttl=300)


def generate_transfer_token(user_id: int) -> str:
    """
    Generate a unique transfer token for a user.

    This function generates a unique token of length 13 characters using UUID version 4 and checked against the cache to ensure uniqueness.

    Args:
        user_id (int): The user ID to associate with the generated token.

    Returns:
        str: A unique transfer token.
    """

    while True:
        token = str(uuid.uuid4())[:13]
        if token not in cache:
            break

    cache[token] = user_id
    return token


def validate_token(token: str) -> int:
    """
    Validate the given transfer token.

    If the token exists in the cache, it returns the associated user ID.

    Args:
        token (str): The transfer token to validate.

    Returns:
        int: The user ID associated with the token if valid; 0 if the token is invalid or expired.
    """
    return cache.get(token, 0)


def invalidate_token(token: str) -> None:
    """
    Invalidate (remove) the given transfer token from the cache.

    Args:
        token (str): The transfer token to invalidate.
    """
    cache.pop(token)
