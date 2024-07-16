from fastapi import APIRouter, Depends

from schemas import BaseST
from exception import duplicate_data, bad_request
from repository.STCRUD import get_st_by_user_id
from authentication.JWTtoken import get_current_user

router = APIRouter(prefix="/st", tags=["Security Target"])


@router.get("/")
async def security_targets(current_user=Depends(get_current_user)) -> list[BaseST]:
    return await get_st_by_user_id(current_user.user_id)
