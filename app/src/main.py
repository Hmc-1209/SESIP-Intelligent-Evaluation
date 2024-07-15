import gradio as gr
from gradio_pdf import PDF
from utils.handlers import *
from utils.placeholders import *


def main():
    """
    The main function of the program.
    :return: none
    """

    results = []
    results = [
        {"id": 1, "summary": "Result 1", "detail": "Detail information for Result 1"},
        {"id": 2, "summary": "Result 2", "detail": "Detail information for Result 2"},
        {"id": 3, "summary": "Result 3", "detail": "Detail information for Result 3"}
    ]

    with gr.Blocks(css="style.css", title="SESIP Eval") as app:
        gr.Markdown("# SESIP Intelligence Eval")
        gr.Markdown("Fast LLM evaluated result will be provided using this tool.")

        # ST upload, detail and evaluation summary
        with gr.Column():
            with gr.Row():
                with gr.Column(elem_classes="app-left"):
                    file_input = PDF(label="Upload PDF", height=750, elem_classes="st_upload")
                with gr.Column(elem_classes="app-right"):
                    file_details = {"md5": "", "sha256": ""}
                    file_md5 = gr.Markdown(st_detail_placeholder(file_details), elem_classes="st_detail_custom")

                    model = gr.Dropdown(label="Select Model", choices=["gpt 3.5", "gpt 4.0"])
                    eval_btn = gr.Button("Process Evaluation")
                    st_evaluation_status = gr.HTML(evaluation_status_placeholder(0))
                    st_evaluation_summary = gr.Markdown(evaluation_summary_placeholder("* ", "* ", "* ", "* "))
            file_input.upload(upload_file, file_input, file_md5)

        # ST evaluation summary detail
        with gr.Column():
            evaluation_result_label = gr.Markdown("# Evaluation Result")
            with gr.Row(elem_classes="app-eval-result"):
                with gr.Column(scale=1, elem_classes="app-eval-result-left"):
                    for result in results:
                        btn = gr.Button(result["summary"], elem_id=str(result["id"]), interactive=True,
                                        elem_classes="app-eval-result-detail-btn")
                with gr.Column(scale=3, elem_classes="app-eval-result-right"):
                    detail_result = gr.Markdown("Click a result to see the detail", elem_id="detail_result")

        with gr.Row():
            save_btn = gr.Button("Save")
            clear_btn = gr.Button("Clear")

    app.launch()


if __name__ == "__main__":
    main()
