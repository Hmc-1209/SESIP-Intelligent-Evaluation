import json
import os
import shutil

from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import FileResponse

from authentication.JWTtoken import get_current_user
from exception import *
from repository.STCRUD import *
from utils.transfer_token_process import validate_token, invalidate_token
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

    filepath = os.path.join(base_path, str(st.st_id), "eval_details.json")
    eval_details = None

    if st.is_evaluated and os.path.isfile(filepath):
        eval_details = json.load(open(filepath, "r"))

    return DetailST(st_id=st.st_id,
                    st_name=st.st_name,
                    st_details=st.st_details,
                    eval_details=eval_details,
                    is_evaluated=st.is_evaluated,
                    eval_passed=st.eval_passed,
                    eval_model=st.eval_model)


@router.get("/file/{st_id}")
async def get_security_target_content(st_id: int, current_user=Depends(get_current_user)) -> FileResponse:
    st = await get_st_by_id(st_id)

    filepath = os.path.join(base_path, str(st.st_id), "st_file.pdf")

    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    if not os.path.isfile(filepath):
        raise no_such_file

    return FileResponse(filepath, media_type="application/pdf")


@router.get("/download/{st_id}")
async def download_eval_file(st_id: int, current_user=Depends(get_current_user)) -> FileResponse:
    st = await get_st_by_id(st_id)

    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    if not st.is_evaluated:
        raise eval_not_performed

    filepath = os.path.join(base_path, str(st.st_id), "eval_file.docx")
    filename = f"{st.st_id}-{st.st_details['TOE_Name']} Evaluation Result.docx"

    if not os.path.isfile(filepath):
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
async def update_security_target(st_id: int, update_st: UpdateST, current_user=Depends(get_current_user)) -> None:
    st = await get_st_by_id(st_id)
    owner_id = validate_token(update_st.token)

    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    if not owner_id:
        raise invalid_token

    if not await update_st_by_id(st_id, owner_id):
        raise bad_request

    invalidate_token(update_st.token)


@router.delete("/{st_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_security_target(st_id: int, current_user=Depends(get_current_user)) -> None:
    st = await get_st_by_id(st_id)
    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    if not await delete_st_by_id(st_id):
        raise bad_request

    dir_path = os.path.join(base_path, str(st_id))

    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
