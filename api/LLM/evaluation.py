import openai
import os
import json

from config import base_path, api_key
from LLM.image_process import get_images_content
from LLM.text_process import get_evaluation_info, get_text_content

eval_result = {"Work_Units": []}
information_position = {}


def call_openai_api(model: str, text: dict, images: list[dict]) -> str:
    openai.api_key = api_key
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": [text] + images}
            ]
        )
        print("Evaluation complete!")

        return response.choices[0].message.content

    except Exception as e:
        print(f"Failed with error {e}")


def get_position(pdf_path: str, model: str, sesip_level: int):
    text = get_evaluation_info(pdf_path, sesip_level)
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, text, images))

    information_position.update(response["Work_Units_Information_Position"])

    del response["Work_Units_Information_Position"]

    eval_result.update(response)


def evaluate_int_and_obj(pdf_path: str, model: str, sesip_level: int):
    filtered = dict(filter(lambda x: "INT" in x[0] or "OBJ" in x[0], information_position.items()))

    text = get_text_content(pdf_path, sesip_level, 1, filtered)
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, text, images))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate_req(pdf_path: str, model: str, sesip_level: int):
    filtered = dict(filter(lambda x: "REQ" in x[0], information_position.items()))

    text = get_text_content(pdf_path, sesip_level, 2, filtered)
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, text, images))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate_tss(pdf_path: str, model: str, sesip_level: int):
    filtered = dict(filter(lambda x: "TSS" in x[0], information_position.items()))

    text = get_text_content(pdf_path, sesip_level, 3, filtered)
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, text, images))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate_flr(pdf_path: str, model: str, sesip_level: int):
    filtered = dict(filter(lambda x: "FLR" in x[0], information_position.items()))

    text = get_text_content(pdf_path, sesip_level, 4, filtered)
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, text, images))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate(st_id: int, model: str, sesip_lv: int):
    dir_path = os.path.join(base_path, str(st_id))
    st_path = os.path.join(dir_path, "st_file.pdf")

    get_position(st_path, model, sesip_lv)
    evaluate_int_and_obj(st_path, model, sesip_lv)
    evaluate_req(st_path, model, sesip_lv)
    evaluate_tss(st_path, model, sesip_lv)
    evaluate_flr(st_path, model, sesip_lv)

    try:
        details_path = os.path.join(dir_path, "eval_result.json")
        with open(details_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(eval_result))
        print("Response written to evaluation-result.json")

    except Exception as e:
        print(f"Failed with error {e}")
