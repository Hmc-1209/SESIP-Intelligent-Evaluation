from models import User
from schemas import CompleteUser
from database import db


async def check_user(user_id: int) -> CompleteUser:
    """
    Check if a user exists by their ID and retrieve their complete information.

    Args:
        user_id (int): The ID of the user to check.

    Returns:
        CompleteUser: An instance of `CompleteUser` containing the user's details if the user exists;
                      otherwise, it may return None if no user with the given ID is found.
    """

    stmt = User.select().where(User.c.user_id == user_id)
    return await db.fetch_one(stmt)
