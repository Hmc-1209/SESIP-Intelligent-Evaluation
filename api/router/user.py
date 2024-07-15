from fastapi import APIRouter, Depends

from schemas import BaseUser,  CompleteUser
from exception import duplicate_data, bad_request
from repository.UserCRUD import get_user_by_name, create_user, update_user
from authentication.JWTtoken import get_current_user
from authentication.hashing import hash_password

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
async def create_new_user(user: BaseUser) -> None:
    if await get_user_by_name(user.username):
        raise duplicate_data

    if not await create_user(user):
        raise bad_request


@router.patch("/")
async def update_current_user(user: BaseUser, current_user: CompleteUser = Depends(get_current_user)) -> None:
    update_data = user.model_dump(exclude_unset=True, exclude_none=True)
    if update_data.get("password"):
        update_data["password"] = hash_password(update_data["password"])
    update = CompleteUser.model_validate(current_user).model_copy(update=update_data)

    if not await update_user(update):
        raise bad_request
