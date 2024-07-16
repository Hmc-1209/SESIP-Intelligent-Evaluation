from fastapi import APIRouter, Depends, status

from schemas import BaseUser, DetailUser, CompleteUser
from exception import duplicate_data, bad_request
from repository.UserCRUD import get_users, get_user_by_name, create_user, update_user, delete_user
from authentication.JWTtoken import get_current_user
from authentication.hashing import hash_password

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


@router.patch("/")
async def update_current_user(user: DetailUser, current_user=Depends(get_current_user)) -> None:
    update_data = user.model_dump(exclude_unset=True, exclude_none=True)

    if update_data.get("username") and await get_user_by_name(update_data["username"]):
        raise duplicate_data

    if update_data.get("password"):
        update_data["password"] = hash_password(update_data["password"])
    update = CompleteUser.model_validate(current_user).model_copy(update=update_data)

    if not await update_user(update):
        raise bad_request


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(current_user=Depends(get_current_user)) -> None:
    if not await delete_user(current_user.user_id):
        raise bad_request
