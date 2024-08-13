import json
import os
from collections import Counter

from exception import evaluation_failed
from schemas import EvaluateST
from utils.file_process import generate_eval_report


def copy_dict(dictionary, keys):
    return {key: dictionary[key] for key in keys}


def count_status_amount(work_units: list):
    counts = Counter([unit["Work_Unit_Evaluation_Result_Status"] for unit in work_units])

    pass_count = counts.get('Pass', 0)
    fail_count = counts.get('Fail', 0)

    return pass_count, fail_count


def extract_data(eval_results: dict):
    st_details = copy_dict(eval_results, ["TOE_Name", "Developer_Organization"])
    eval_details = copy_dict(eval_results, ["Work_Units"])

    eval_details["Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status"] = count_status_amount(
        eval_results["Work_Units"]
    )

    return st_details, eval_details


def parse_eval_result(dir_path: str) -> EvaluateST:
    try:
        eval_results = json.load(open(os.path.join(dir_path, 'eval_result.json'), 'r', encoding='utf-8'))

        st_details, eval_details = extract_data(eval_results)
        eval_passed = not eval_details["Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status"][1]

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
