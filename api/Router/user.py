from fastapi import APIRouter, Depends

from schemas import BaseUser
from exception import duplicate_data, bad_request
from Repository.UserCRUD import get_user_by_name, create_user
from Authentication.JWTtoken import get_current_user
from Authentication.hashing import hash_password

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
async def create_new_user(user: BaseUser) -> None:
    if await get_user_by_name(user.username):
        raise duplicate_data

    if not await create_user(user):
        raise bad_request
