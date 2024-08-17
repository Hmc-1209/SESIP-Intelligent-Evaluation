import json
import os

import openai

from LLM.image_process import Images
from LLM.text_process import Text
from config import base_path, api_key

text = Text()
images = Images()
eval_result = {"Work_Units": []}
information_position = {}


def call_openai_api(model: str) -> str:
    openai.api_key = api_key
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": [text.prompt] + images.images}
            ]
        )
        print("Evaluation complete!")

        return response.choices[0].message.content

    except Exception as e:
        print(f"Failed with error {e}")


def get_position(model: str):
    text.get_evaluation_info()
    response = json.loads(call_openai_api(model))

    information_position.update(response["Work_Units_Information_Position"])

    del response["Work_Units_Information_Position"]

    eval_result.update(response)


def evaluate_int_and_obj(model: str):
    filtered = dict(filter(lambda x: "INT" in x[0] or "OBJ" in x[0], information_position.items()))

    text.get_text_content(filtered)
    response = json.loads(call_openai_api(model))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate_req(model: str):
    filtered = dict(filter(lambda x: "REQ" in x[0], information_position.items()))

    text.get_text_content(filtered)
    response = json.loads(call_openai_api(model))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate_tss(model: str):
    filtered = dict(filter(lambda x: "TSS" in x[0], information_position.items()))

    text.get_text_content(filtered)
    response = json.loads(call_openai_api(model))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate_flr(model: str):
    filtered = dict(filter(lambda x: "FLR" in x[0], information_position.items()))

    text.get_text_content(filtered)
    response = json.loads(call_openai_api(model))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate(st_id: int, model: str, sesip_lv: int):
    dir_path = os.path.join(base_path, str(st_id))
    st_path = os.path.join(dir_path, "st_file.pdf")

    text.update_st(st_path, sesip_lv)
    images.update_st(st_path)

    get_position(model)
    evaluate_int_and_obj(model)
    evaluate_req(model)
    evaluate_tss(model)
    evaluate_flr(model)

    try:
        details_path = os.path.join(dir_path, "eval_result.json")
        with open(details_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(eval_result))
        print("Response written to evaluation-result.json")

    except Exception as e:
        print(f"Failed with error {e}")
