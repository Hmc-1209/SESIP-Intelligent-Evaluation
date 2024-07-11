import gradio as gr
import fitz


def upload_file(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


demo = gr.Interface(
    title="SESIP Intelligence Eval",
    description="Fast LLM evaluated result will be provide using this tool.",
    fn=upload_file,
    inputs=[gr.File(label="Upload ST")],
    outputs=[gr.Textbox(label="PDF content", lines=10)],
)

demo.launch()
