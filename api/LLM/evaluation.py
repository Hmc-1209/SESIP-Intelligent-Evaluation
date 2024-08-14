import openai
import os

from config import base_path, api_key
from utils.pdf_image_process import get_images_content
from utils.pdf_text_process import get_text_content


def evaluate(st_id: int, model: str, sesip_lv: int):
    dir_path = os.path.join(base_path, str(st_id))
    st_path = os.path.join(dir_path, "st_file.pdf")

    text = get_text_content(st_path, sesip_lv)
    images = get_images_content(st_path)
    openai.api_key = api_key

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": [text] + images}
            ]
        )
        response_text = response.choices[0].message.content
        print("Evaluation complete!")

        details_path = os.path.join(dir_path, "eval_result.json")
        with open(details_path, "w", encoding="utf-8") as f:
            f.write(response_text)
        print("Response written to evaluation-result.json")

    except Exception as e:
        print(f"Failed with error {e}")
