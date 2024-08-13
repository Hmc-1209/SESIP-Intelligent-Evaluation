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
    """
    Evaluate the specified Security Target (ST) and generate evaluation results.

    Args:
        st_id (int): The ID of the Security Target to be evaluated.
        eval_model (str): The evaluation model to use for the evaluation.
        sesip_level (int): The SESIP level for the evaluation.
        current_user (CompleteUser): The currently authenticated user.

    Returns:
        EvaluateST: An instance of `EvaluateST` containing the evaluation results.

    Raises:
        no_such_st: If the Security Target does not exist.
        st_not_belongs: If the Security Target does not belong to the current user.
        eval_has_performed: If the Security Target has already been evaluated.
        invalid_model: If the provided evaluation model is not valid.
        invalid_level: If the SESIP level is not valid.
        bad_request: If updating the Security Target in the database fails.
    """

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
