import gradio as gr
from gradio_pdf import PDF
from utils.handlers import *
from utils.placeholders import *


def main():
    """
    The main function of the program.
    :return: none
    """
    with gr.Blocks(css="style.css") as app:
        gr.Markdown("# SESIP Intelligence Eval")
        gr.Markdown("Fast LLM evaluated result will be provided using this tool.")

        with gr.Row():
            with gr.Column(elem_classes="app-left"):
                file_input = PDF(label="Upload PDF", height=800, elem_classes="st_upload")
            with gr.Column(elem_classes="app-right"):

                file_details = {"md5": "", "sha256": ""}
                file_md5 = gr.Markdown(st_detail_placeholder(file_details), elem_classes="st_detail_custom")

                model = gr.Dropdown(label="Select Model", choices=["gpt 3.5", "gpt 4.0"])
                eval_btn = gr.Button("Process Evaluation")
                assessment_status = gr.HTML(assessment_status_placeholder(0))

        file_input.upload(upload_file, file_input, file_md5)

    app.launch()


if __name__ == "__main__":
    main()
