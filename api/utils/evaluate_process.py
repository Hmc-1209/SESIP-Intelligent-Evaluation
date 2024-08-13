import json
import os
from collections import Counter

from exception import evaluation_failed
from schemas import EvaluateST
from utils.file_process import generate_eval_report


def copy_dict(dictionary, keys) -> dict:
    """
    Create a new dictionary by copying selected keys and their values from the given dictionary.

    Args:
        dictionary (dict): The source dictionary to copy from.
        keys (list): The list of keys to be copied.

    Returns:
        dict: A new dictionary with the selected keys and their corresponding values.
    """
    return {key: dictionary[key] for key in keys}


def count_status_amount(work_units: list) -> tuple[int, int]:
    """
    Count the number of 'Pass' and 'Fail' statuses in a list of work units.

    Args:
        work_units (list): A list of work units, each containing an evaluation result status.

    Returns:
        tuple: A tuple with two integers representing the number of 'Pass' and 'Fail' statuses, respectively.
    """

    counts = Counter([unit["Work_Unit_Evaluation_Result_Status"] for unit in work_units])

    pass_count = counts.get('Pass', 0)
    fail_count = counts.get('Fail', 0)

    return pass_count, fail_count


def extract_data(eval_results: dict) -> tuple[dict, dict]:
    """
    Extract and organize data from the evaluation results.

    Args:
        eval_results (dict): The dictionary containing evaluation results.

    Returns:
        tuple: A tuple containing two dictionaries:
            - st_details: Details about the Security Target (ST).
            - eval_details: Detailed evaluation results including the work units' name, description, and pass/fail counts.
    """

    st_details = copy_dict(eval_results, ["TOE_Name", "Developer_Organization"])
    eval_details = copy_dict(eval_results, ["Work_Units"])

    eval_details["Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status"] = count_status_amount(
        eval_results["Work_Units"]
    )

    return st_details, eval_details


def parse_eval_result(dir_path: str) -> EvaluateST:
    """
    Parse evaluation results from a JSON file and return an `EvaluateST` instance.

    Args:
        dir_path (str): The directory path where the evaluation result JSON file is located.

    Returns:
        EvaluateST: An instance of `EvaluateST` containing the parsed evaluation results.

    Raises:
        evaluation_failed: If an error occurs while parsing the evaluation results.
    """

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
    """
    Generate files for the evaluation results, including the evaluation details JSON and a DOCX report.

    Args:
        dir_path (str): The directory path where the files will be saved.
        st (EvaluateST): An instance of `EvaluateST` containing the evaluation results.

    Raises:
        evaluation_failed: If an error occurs while parsing the evaluation results.
    """

    try:
        # Save Evaluation Details file
        with open(os.path.join(dir_path, 'eval_details.json'), "w", encoding="utf-8") as f:
            f.write(json.dumps(st.eval_details))

        # Generate Evaluation Report Docx
        generate_eval_report(dir_path, st.st_details["SESIP_Level"])

    except Exception as e:
        print(f"Error: {e}")
        raise evaluation_failed
