from fastapi import APIRouter, Depends, status

from schemas import BaseUser, DetailUser, UpdateUser, CompleteUser
from exception import duplicate_data, bad_request, password_incorrect
from repository.UserCRUD import get_users, get_user_by_name, create_user, update_username, update_password, delete_user
from authentication.JWTtoken import get_current_user
from authentication.hashing import verify_password

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/")
async def users(_=Depends(get_current_user)) -> list[BaseUser]:
    return await get_users()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: DetailUser) -> None:
    if await get_user_by_name(user.username):
        raise duplicate_data

    if not await create_user(user):
        raise bad_request


@router.patch("/update_username")
async def update_user_username(user: BaseUser, current_user=Depends(get_current_user)) -> None:
    if await get_user_by_name(user.username):
        raise duplicate_data

    if not await update_username(current_user.user_id, user):
        raise bad_request


@router.patch("/update_password")
async def update_user_password(user: UpdateUser, current_user=Depends(get_current_user)) -> None:
    if not await update_password(current_user.user_id, user):
        raise bad_request


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(current_user=Depends(get_current_user)) -> None:
    if not await delete_user(current_user.user_id):
        raise bad_request
