from fastapi import APIRouter, Depends, status

from authentication.JWTtoken import get_current_user
from exception import duplicate_data, bad_request, no_such_user, no_such_st, st_not_belongs
from repository.STCRUD import get_st_by_id, get_st_by_name, get_st_by_user_id, update_st_by_id, delete_st_by_id
from repository.UserCRUD import get_user_by_id
from schemas import ListST, DetailST, UpdateST

router = APIRouter(prefix="/st", tags=["Security Target"])


@router.get("/")
async def security_targets(current_user=Depends(get_current_user)) -> list[ListST]:
    return await get_st_by_user_id(current_user.user_id)


@router.get("/{st_id}")
async def get_detail_security_target(st_id: int, current_user=Depends(get_current_user)) -> DetailST:
    st = await get_st_by_id(st_id)
    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    return st


@router.get("/download/{st_id}")
async def download_eval_file(st_id: int, current_user=Depends(get_current_user)) -> str:
    st = await get_st_by_id(st_id)
    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    return st.eval_file


@router.patch("/{st_id}")
async def update_security_target(st_id: int, new_st: UpdateST, current_user=Depends(get_current_user)) -> None:
    st = await get_st_by_id(st_id)
    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    update_data = new_st.model_dump(exclude_unset=True, exclude_none=True)

    if update_data.get("st_name") and await get_st_by_name(update_data["st_name"]):
        raise duplicate_data

    if update_data.get("owner_id") and not await get_user_by_id(update_data["owner_id"]):
        raise no_such_user

    update = UpdateST.model_validate(st).model_copy(update=update_data)

    if not await update_st_by_id(st_id, update):
        raise bad_request


@router.delete("/{st_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_security_target(st_id: int, current_user=Depends(get_current_user)) -> None:
    st = await get_st_by_id(st_id)
    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    if not await delete_st_by_id(st_id):
        raise bad_request
