import gradio as gr


with gr.Blocks(css="style.css", title="SESIP Eval") as app:
    gr.Markdown("# SESIP Intelligence Evaluator", elem_classes="login_page_title")
    with gr.Row(elem_classes="login_page_main_app"):
        with gr.Tab("Login", elem_classes="login_form"):
            with gr.Column():
                gr.Textbox(label="Username", placeholder="Enter your username", interactive=True)
                gr.Textbox(label="Password", placeholder="Enter your password", interactive=True)
                gr.Button("Login")

        with gr.Tab("Sign Up", elem_classes="signup_form"):
            with gr.Column():
                gr.Textbox(label="Username", placeholder="Enter your username", interactive=True)
                gr.Textbox(label="Password", placeholder="Enter your password", interactive=True)
                gr.Button("Sign Up")
