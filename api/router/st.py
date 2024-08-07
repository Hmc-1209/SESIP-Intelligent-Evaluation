from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import FileResponse
import os

from authentication.JWTtoken import get_current_user
from exception import bad_request, no_such_user, no_such_st, no_such_file, st_not_belongs
from repository.STCRUD import *
from repository.UserCRUD import get_user_by_id
from schemas import ListST, DetailST, UpdateST
from config import base_path

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
async def download_eval_file(st_id: int, current_user=Depends(get_current_user)) -> FileResponse:
    st = await get_st_by_id(st_id)

    filepath = os.path.join(base_path, str(st.st_id), "eval_file.docx")
    filename = f"{st.st_id}-{st.st_details['TOE_NAME']} Evaluation Result.docx"

    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    if not st.is_evaluated or not os.path.isfile(filepath):
        raise no_such_file

    return FileResponse(filepath, media_type='application/octet-stream', filename=filename)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_security_target(new_st: UploadFile, current_user=Depends(get_current_user)) -> int:
    st_id = await create_st(os.path.splitext(new_st.filename)[0], current_user.user_id)

    if not st_id:
        raise bad_request

    dir_path = os.path.join(base_path, str(st_id))
    filepath = os.path.join(dir_path, "st_file.pdf")

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(filepath, "wb") as f:
        f.write(await new_st.read())

    return st_id


@router.patch("/{st_id}")
async def update_security_target(st_id: int, new_st: UpdateST, current_user=Depends(get_current_user)) -> None:
    st = await get_st_by_id(st_id)
    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    update_data = new_st.model_dump(exclude_unset=True, exclude_none=True)

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
