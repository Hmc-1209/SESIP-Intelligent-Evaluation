import gradio as gr
import fitz


def upload_file(file):
    text = ""
    with fitz.open(file) as doc:
        for page in doc:
            text += page.get_text()
    return text


with gr.Blocks() as demo:
    gr.Markdown("# SESIP Intelligence Eval")
    gr.Markdown("Fast LLM evaluated result will be provided using this tool.")

    with gr.Column():
        with gr.Row():
            file_input = gr.File(label="Upload PDF")
            file_detail = gr.Markdown("## Security Target details", height=500)
        pdf_content = gr.Textbox(label="PDF content", lines=10)

    file_input.upload(upload_file, file_input, pdf_content)

demo.launch()
