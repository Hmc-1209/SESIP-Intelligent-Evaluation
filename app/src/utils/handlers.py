import fitz
import hashlib
from utils.placeholders import st_detail_placeholder


def upload_file(file):
    """
    Upload Security Target file

    This function take a file upload and returns the st detail

    :param file: string, the content of the uploaded st file
    :return: detail_message: string, st detail information in Markdown format
    """

    text = ""
    with fitz.open(file) as doc:
        for page in doc:
            text += page.get_text()

    file_content = open(file, 'rb').read()
    md5_value = hashlib.md5(file_content).hexdigest()
    sha256_value = hashlib.sha256(file_content).hexdigest()

    detail_message = st_detail_placeholder({"md5": md5_value, "sha256": sha256_value})

    return detail_message
