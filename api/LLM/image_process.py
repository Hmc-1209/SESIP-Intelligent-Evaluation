import base64
import io

import fitz
from PIL import Image


def api_image_structure(base64_img: str) -> dict:
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_img}",
            "detail": "low"
        }
    }


class Images:
    def __init__(self, st_path: str):
        self._st = fitz.open(st_path)
        self._images = self._get_base64_images()

    @property
    def images(self):
        return self._images

    def _extract_pdf_images_info(self):
        images = []
        for page_number in range(len(self._st)):
            page = self._st[page_number]
            images += page.get_images(full=True)

        return images

    def _extract_pdf_image(self, xref: int):
        image_data = self._st.extract_image(xref)["image"]

        with Image.open(io.BytesIO(image_data)) as img:
            resized_image = img.resize((512, 512))

            buffered = io.BytesIO()
            resized_image.save(buffered, format="JPEG")

        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def _get_base64_images(self):
        base64_image_list = []
        for image in self._extract_pdf_images_info():
            base64_img = self._extract_pdf_image(image[0])
            base64_image_list.append(base64_img)

        return base64_image_list
