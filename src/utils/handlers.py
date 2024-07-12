import fitz
import hashlib
from utils.placeholders import st_detail_placeholder


def upload_file(file):
    """
    Send the uploaded st information to get the content and detail displayed

    This function take a file upload and returns the st detail and contents

    :param file: str
    :return: text: st content, detail_message: st detail information
    """

    text = ""
    with fitz.open(file) as doc:
        for page in doc:
            text += page.get_text()

    md5_value = hashlib.md5(open(file, 'rb').read()).hexdigest()
    detail_message = st_detail_placeholder(md5_value)

    return text, detail_message
