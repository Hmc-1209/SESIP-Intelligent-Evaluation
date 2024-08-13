from authentication import JWTtoken
from models import User
from schemas import CompleteUser
from database import db


async def generate_access_token(data: dict) -> str:
    """
    Generate an access token for the user based on provided credentials.

    Args:
        data (dict): A dictionary containing 'username' and 'password' of the user.

    Returns:
        str: An access token if the credentials are valid; otherwise, an empty string.
    """

    stmt = User.select().where(User.c.username == data["username"])
    user = await db.fetch_one(stmt)

    if user:
        if JWTtoken.verify_password(data["password"], user.password):
            data["id"] = user.user_id
            del data["password"]
            return JWTtoken.generate_access_token(data)

    return ""


async def validate_access_token(token: str) -> CompleteUser:
    """
    Validate an access token and retrieve the corresponding user information.

    Args:
        token (str): The access token to validate.

    Returns:
        CompleteUser: The user details associated with the token if valid; otherwise, raises an exception.
    """

    return await JWTtoken.get_current_user(token)
