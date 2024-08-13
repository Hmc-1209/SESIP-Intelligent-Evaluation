from fastapi import APIRouter, Depends

import os

from authentication.JWTtoken import get_current_user
from exception import *
from repository.STCRUD import *
from LLM.evaluation import evaluate
from utils.evaluate_process import parse_eval_result, generate_files
from schemas import EvaluateST
from config import base_path

router = APIRouter(prefix="/eval", tags=["Evaluation"])


@router.post("/{st_id}", status_code=status.HTTP_201_CREATED)
async def evaluate_security_target(st_id: int, eval_model: str, sesip_level: int,
                                   current_user=Depends(get_current_user)) -> EvaluateST:
    # Validation
    st = await get_st_by_id(st_id)
    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    if st.is_evaluated:
        raise eval_has_performed

    if eval_model not in ["gpt-4o-mini"]:
        raise invalid_model

    if sesip_level not in [1, 2]:
        raise invalid_level

    # Evaluation
    evaluate(st_id, eval_model, sesip_level)

    dir_path = os.path.join(base_path, str(st_id))
    update_st = parse_eval_result(dir_path)

    update_st.st_details["SESIP_Level"] = sesip_level
    update_st.eval_model = eval_model

    generate_files(dir_path, update_st)

    # Update the data in db
    if not await update_st_after_eval(st_id, update_st):
        raise bad_request

    return update_st
