from fastapi import Depends
from datetime import timedelta, datetime
from jose import jwt, JWTError

from repository.CommonCRUD import check_user
from authentication.hashing import verify_password
from authentication.OAuth2 import oauth2_token_scheme
from config import access_token_secret_key, algorithm, access_token_expire_days
from exception import validation_failed, token_expired


def generate_access_token(data: dict):
    """
    Generate a JWT access token with an expiration time.

    Args:
        data (dict): The user identification information to include in the token.

    Returns:
        str: The generated JWT access token.
    """

    data["exp"] = datetime.utcnow() + timedelta(days=int(access_token_expire_days))
    token = jwt.encode(data, access_token_secret_key, algorithm=algorithm)

    return token


async def get_current_user(token=Depends(oauth2_token_scheme)):
    """
    Extract and return the current user from the JWT token.

    Args:
        token (str): The JWT token extracted from the request's Authorization header.

    Returns:
        CompleteUser: The user details extracted from the token.

    Raises:
        validation_failed: If the token is invalid or the user is not found.
        token_expired: If the token has expired.
    """

    try:
        payload = jwt.decode(
            token, access_token_secret_key, algorithms=algorithm)

        user = await check_user(payload["id"])

        if not user:
            raise validation_failed

        return user

    except JWTError:
        raise token_expired
