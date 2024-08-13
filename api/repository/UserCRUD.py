from authentication.hashing import hash_password
from database import db, execute_stmt_in_tran
from models import User, SecurityTarget
from schemas import BaseUser, DetailUser, UpdateUser
from authentication.hashing import hash_password


async def get_user_by_name(username: str) -> BaseUser:
    """
    Retrieve a user from the database by their username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        BaseUser: The user object if found; otherwise, returns None.
    """

    stmt = User.select().where(User.c.username == username)
    return await db.fetch_one(stmt)


async def create_user(user: DetailUser) -> bool:
    """
    Create a new user in the database with the given details.

    Args:
        user (DetailUser): The details of the user to create, including username and password.

    Returns:
        bool: True if the user was successfully created; False otherwise.
    """

    stmt = User.insert().values(username=user.username,
                                password=hash_password(user.password))
    return await execute_stmt_in_tran([stmt])


async def update_username(user_id: int, user: BaseUser) -> bool:
    """
    Update the username of an existing user.

    Args:
        user_id (int): The ID of the user to update.
        user (BaseUser): The new username to set.

    Returns:
        bool: True if the username was successfully updated; False otherwise.
    """

    stmt = User.update().where(User.c.user_id == user_id).values(username=user.username)
    return await execute_stmt_in_tran([stmt])


async def update_password(user_id: int, user: UpdateUser) -> bool:
    """
    Update the password of an existing user.

    Args:
        user_id (int): The ID of the user to update.
        user (UpdateUser): The new password to set.

    Returns:
        bool: True if the password was successfully updated; False otherwise.
    """

    stmt = User.update().where(User.c.user_id == user_id).values(password=hash_password(user.new_password))
    return await execute_stmt_in_tran([stmt])


async def delete_user(user_id: int) -> bool:
    """
    Delete a user and their associated security targets from the database.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        bool: True if the user and their security targets were successfully deleted; False otherwise.
    """

    stmt1 = SecurityTarget.delete().where(SecurityTarget.c.owner_id == user_id)
    stmt2 = User.delete().where(User.c.user_id == user_id)
    return await execute_stmt_in_tran([stmt1, stmt2])
