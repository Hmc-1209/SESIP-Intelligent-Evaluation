from collections import Counter

from fastapi import APIRouter, Depends, status

import os
import json

from authentication.JWTtoken import get_current_user
from exception import *
from repository.STCRUD import *
from LLM.evaluation import evaluate
from utils.file_process import generate_eval_report
from schemas import EvaluateST
from config import base_path

router = APIRouter(prefix="/eval", tags=["Evaluation"])


def copy_dict(dictionary, keys):
    return {key: dictionary[key] for key in keys}


def parse_eval_result(dir_path: str) -> EvaluateST:
    try:
        eval_results = json.load(open(os.path.join(dir_path, 'eval_result.json'), 'r', encoding='utf-8'))

        st_details = copy_dict(eval_results, ["TOE_Name", "Developer_Organization"])
        eval_details = copy_dict(eval_results, ["Work_Units"])

        counts = Counter([unit["Work_Unit_Evaluation_Result_Status"] for unit in eval_results["Work_Units"]])

        pass_count = counts.get('Pass', 0)
        fail_count = counts.get('Fail', 0)

        eval_details["Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status"] = [pass_count, fail_count]

        eval_passed = False if eval_details["Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status"][1] else True

        return EvaluateST(st_details=st_details,
                          eval_details=eval_details,
                          eval_passed=eval_passed,
                          eval_model="")

    except Exception as e:
        print(f"Error: {e}")
        raise evaluation_failed


def generate_files(dir_path: str, st: EvaluateST) -> None:
    try:
        # Save Evaluation Details file
        with open(os.path.join(dir_path, 'eval_details.json'), "w", encoding="utf-8") as f:
            f.write(json.dumps(st.eval_details))

        # Generate Evaluation Docx
        generate_eval_report(dir_path, st.st_details["SESIP_Level"])
    except Exception as e:
        print(f"Error: {e}")


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
