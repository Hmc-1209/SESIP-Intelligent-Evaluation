from fastapi import APIRouter, Depends, status

import os
import json

from authentication.JWTtoken import get_current_user
from exception import bad_request, no_such_st, st_not_belongs, eval_has_performed, evaluation_failed
from repository.STCRUD import *
from LLM.evaluation import evaluate
from schemas import EvaluateST
from config import base_path

router = APIRouter(prefix="/eval", tags=["Evaluation"])


def copy_dict(dictionary, keys):
    return {key: dictionary[key] for key in keys}


@router.post("/{st_id}", status_code=status.HTTP_201_CREATED)
async def evaluate_security_target(st_id: int, current_user=Depends(get_current_user)) -> EvaluateST:
    # Validation
    st = await get_st_by_id(st_id)
    if not st:
        raise no_such_st

    if not current_user.user_id == st.owner_id:
        raise st_not_belongs

    if st.is_evaluated:
        raise eval_has_performed

    # Evaluation
    evaluate(st_id)

    # Parsing
    try:
        dir_path = os.path.join(base_path, str(st_id))
        eval_results = json.load(open(os.path.join(dir_path, 'eval_result.json'), 'r', encoding='utf-8'))

        st_details = copy_dict(eval_results, ["TOE_Name", "Developer_Organization", "SESIP_Level"])
        eval_details = copy_dict(eval_results, ["Work_Units", "Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status"])
        is_valid = False if eval_results["Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status"][1] else True

    except Exception as e:
        print(f"Error: {e}")
        raise evaluation_failed

    # Save Evaluation Details file
    with open(os.path.join(dir_path, 'eval_details.json'), "w", encoding="utf-8") as f:
        f.write(json.dumps(eval_details))

    # Update the data in db
    if not await update_st_after_eval(st_id, st_details, is_valid):
        raise bad_request

    return EvaluateST(st_details=st_details,
                      eval_details=eval_details,
                      is_valid=is_valid)
