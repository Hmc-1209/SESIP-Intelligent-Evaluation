import json
import os

import openai

from LLM.image_process import Images
from LLM.text_process import Text
from config import base_path, api_key


class Evaluation:
    position_filter = {0: ["INT", "OBJ"], 1: ["REQ"], 2: ["TSS"], 3: ["FLR"]}

    def __init__(self, st_path: str, sesip_level: int, model: str):
        self._text = Text(st_path, sesip_level)
        self._images = Images(st_path)
        self._model = model

        self._step = 0

        self._information_position = {}
        self._eval_result = {"Work_Units": []}

    @property
    def eval_result(self):
        return self._eval_result

    def call_openai_api(self) -> str:
        openai.api_key = api_key
        try:
            response = openai.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "user", "content": [self._text.prompt] + self._images.images}
                ]
            )
            print("Evaluation complete!")

            return response.choices[0].message.content

        except Exception as e:
            print(f"Call Openai API Error: {e}")

    def get_position(self):
        self._text.get_evaluation_info()
        response = json.loads(self.call_openai_api())

        self._information_position.update(response["Work_Units_Information_Position"])
        del response["Work_Units_Information_Position"]

        self._eval_result.update(response)

    def evaluate_units(self):
        while self._step < 4:
            try:
                filters = self.__class__.position_filter[self._step]
                filtered = {k: v for k, v in self._information_position.items() if any(f in k for f in filters)}
                self._text.get_text_content(filtered, self._step)

                response = json.loads(self.call_openai_api())
                self._eval_result["Work_Units"] += response["Evaluation_Result"]

                self._step += 1
            except Exception as e:
                print(f"Evaluate Units Error: {e}")


def evaluate(st_id: int, model: str, sesip_level: int):
    dir_path = os.path.join(base_path, str(st_id))
    st_path = os.path.join(dir_path, "st_file.pdf")

    evaluation = Evaluation(st_path, sesip_level, model)
    evaluation.get_position()
    evaluation.evaluate_units()

    try:
        details_path = os.path.join(dir_path, "eval_result.json")
        with open(details_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(evaluation.eval_result))
        print("Response written to evaluation-result.json")

    except Exception as e:
        print(f"Evaluate Error: {e}")
