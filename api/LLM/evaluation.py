import openai
import os
import json

from config import base_path, api_key
from LLM.image_process import get_images_content
from LLM.text_process import Text

text = Text()
eval_result = {"Work_Units": []}
information_position = {}


def call_openai_api(model: str, images: list[dict]) -> str:
    openai.api_key = api_key
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": [text.prompt] + images}
            ]
        )
        print("Evaluation complete!")

        return response.choices[0].message.content

    except Exception as e:
        print(f"Failed with error {e}")


def get_position(pdf_path: str, model: str):
    text.get_evaluation_info()
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, images))

    information_position.update(response["Work_Units_Information_Position"])

    del response["Work_Units_Information_Position"]

    eval_result.update(response)


def evaluate_int_and_obj(pdf_path: str, model: str):
    filtered = dict(filter(lambda x: "INT" in x[0] or "OBJ" in x[0], information_position.items()))

    text.get_text_content(filtered)
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, images))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate_req(pdf_path: str, model: str):
    filtered = dict(filter(lambda x: "REQ" in x[0], information_position.items()))

    text.get_text_content(filtered)
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, images))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate_tss(pdf_path: str, model: str):
    filtered = dict(filter(lambda x: "TSS" in x[0], information_position.items()))

    text.get_text_content(filtered)
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, images))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate_flr(pdf_path: str, model: str):
    filtered = dict(filter(lambda x: "FLR" in x[0], information_position.items()))

    text.get_text_content(filtered)
    images = get_images_content(pdf_path)
    response = json.loads(call_openai_api(model, images))

    eval_result["Work_Units"] += response["Evaluation_Result"]


def evaluate(st_id: int, model: str, sesip_lv: int):
    dir_path = os.path.join(base_path, str(st_id))
    st_path = os.path.join(dir_path, "st_file.pdf")
    text.update_st(st_path, sesip_lv)

    get_position(st_path, model)
    evaluate_int_and_obj(st_path, model)
    evaluate_req(st_path, model)
    evaluate_tss(st_path, model)
    evaluate_flr(st_path, model)

    try:
        details_path = os.path.join(dir_path, "eval_result.json")
        with open(details_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(eval_result))
        print("Response written to evaluation-result.json")

    except Exception as e:
        print(f"Failed with error {e}")
