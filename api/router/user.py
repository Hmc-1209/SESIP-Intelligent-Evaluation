import os
import shutil
from fastapi import APIRouter, Depends, status

from schemas import BaseUser, DetailUser, UpdateUser, CompleteUser
from exception import duplicate_data, bad_request, password_incorrect
from repository.UserCRUD import get_user_by_name, create_user, update_username, update_password, delete_user
from repository.STCRUD import get_st_by_user_id
from repository.TokenCRUD import update_access_token
from authentication.JWTtoken import get_current_user
from authentication.hashing import verify_password
from config import base_path

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: DetailUser) -> None:
    """
    Create a new user.

    This endpoint creates a new user with the details provided in the request body.
    If a user with the given username already exists, a duplicate_data exception is raised.

    Args:
        user (DetailUser): The details (username, password) of the user to be created.

    Raises:
        duplicate_data: If a user with the given username already exists.
        bad_request: If there is an issue with the request or user creation fails.
    """

    if await get_user_by_name(user.username):
        raise duplicate_data

    if not await create_user(user):
        raise bad_request


@router.patch("/update_username")
async def update_user_username(user: BaseUser, current_user=Depends(get_current_user)) -> str:
    """
    Update the username of the current user (requires authentication).

    This endpoint updates the username of the currently authenticated user with the username provided in the request body.
    If the new username already exists, a duplicate_data exception is raised.

    Args:
        user (BaseUser): The new username to update.
        current_user (CompleteUser): The currently authenticated user.
    Returns:
        str: Updated token with updated username.
    Raises:
        duplicate_data: If the new username is already taken.
        bad_request: If there is an issue with the request or username update fails.
    """

    if await get_user_by_name(user.username):
        raise duplicate_data

    if not await update_username(current_user.user_id, user):
        raise bad_request

    return await update_access_token({"username": user.username})


@router.patch("/update_password")
async def update_user_password(user: UpdateUser, current_user=Depends(get_current_user)) -> None:
    """
    Update the password of the current user (requires authentication).

    This endpoint updates the password of the currently authenticated user. The request must include the old password and the new password.
    If the old password does not match the current password, a password_incorrect exception is raised.

    Args:
        user (UpdateUser): The old and new passwords for the user.
        current_user (CompleteUser): The currently authenticated user.

    Raises:
        password_incorrect: If the old password is incorrect.
        bad_request: If there is an issue with the request or password update fails.
    """

    if not verify_password(user.old_password, current_user.password):
        raise password_incorrect

    if not await update_password(current_user.user_id, user):
        raise bad_request


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(current_user=Depends(get_current_user)) -> None:
    """
    Delete the current user (requires authentication).

    This endpoint deletes the currently authenticated user.
    If there is an issue with the deletion, a bad_request exception is raised.

    Args:
        current_user (CompleteUser): The currently authenticated user.

    Raises:
        bad_request: If there is an issue with the request or user deletion fails.
    """

    st_list = await get_st_by_user_id(current_user.user_id)

    if not await delete_user(current_user.user_id):
        raise bad_request

    if not st_list:
        return

    for st in st_list:
        dir_path = os.path.join(base_path, str(st.st_id))
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
