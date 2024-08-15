import fitz
from PIL import Image
import io
import base64


def extract_pdf_images(pdf_file: fitz.Document) -> list[tuple]:
    images = []
    for page_number in range(len(pdf_file)):
        page = pdf_file[page_number]
        images += page.get_images(full=True)

    return images


def resize_image(image_bytes: bytes):
    return Image.open(io.BytesIO(image_bytes)).resize((512, 512))


def base64_image(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def api_image_structure(base64_img: str) -> dict:
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_img}",
            "detail": "low"
        }
    }


def get_images_content(pdf_path: str):
    pdf_document = fitz.open(pdf_path)
    images = extract_pdf_images(pdf_document)

    base64_image_list = []
    for image in images:
        base_image = pdf_document.extract_image(image[0])["image"]
        image = resize_image(base_image)
        base64_img = base64_image(image)

        base64_image_list.append(api_image_structure(base64_img))

    return base64_image_list
