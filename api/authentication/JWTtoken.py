from fastapi import Depends
from datetime import timedelta, datetime
from jose import jwt, JWTError

from repository.CommonCRUD import check_user
from authentication.hashing import verify_password
from authentication.OAuth2 import oauth2_token_scheme
from config import access_token_secret_key, algorithm, access_token_expire_days
from exception import no_such_user, token_expired


def generate_access_token(data: dict):
    """Generate access_token"""

    data["exp"] = datetime.utcnow() + timedelta(days=int(access_token_expire_days))
    token = jwt.encode(data, access_token_secret_key, algorithm=algorithm)

    return token


async def get_current_user(token=Depends(oauth2_token_scheme)):
    """Get the current user's info, also used for authenticate JWT"""

    try:
        payload = jwt.decode(
            token, access_token_secret_key, algorithms=algorithm)

        user = await check_user(payload["id"])

        if user:
            if verify_password(payload["password"], user.password):
                return user

        raise no_such_user

    except JWTError:
        raise token_expired
