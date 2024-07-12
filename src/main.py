import gradio as gr
from gradio_pdf import PDF
import fitz
import hashlib


def upload_file(file):
    text = ""
    with fitz.open(file) as doc:
        for page in doc:
            text += page.get_text()
    md5_value = hashlib.md5(open(file, 'rb').read()).hexdigest()
    return text, md5_value


with gr.Blocks() as demo:
    gr.Markdown("# SESIP Intelligence Eval")
    gr.Markdown("Fast LLM evaluated result will be provided using this tool.")

    with gr.Column():
        with gr.Row():
            file_input = PDF(label="Upload PDF")
            with gr.Column():
                file_detail = gr.Markdown("## Security Target details", height=500)
                file_md5 = gr.Textbox(label="MD5 checksum")
        pdf_content = gr.Textbox(label="PDF content", lines=10)

    file_input.upload(upload_file, file_input, [pdf_content, file_md5])

demo.launch()
