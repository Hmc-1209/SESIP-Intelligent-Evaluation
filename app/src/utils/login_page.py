import gradio as gr


with gr.Blocks(css="style.css", title="SESIP Eval", elem_classes="login_page") as app:
    gr.Markdown("# SESIP Intelligence Evaluator", elem_classes="login_page_title")
    with gr.Row(elem_classes="login_page_main_app"):
        with gr.Tab(label="Login", elem_classes="login_form"):
            gr.Textbox(label="Username", placeholder="Enter your username", interactive=True)
            gr.Textbox(label="Password", placeholder="Enter your password", interactive=True)
            gr.Button("Login")

        with gr.Tab(label="Sign Up", elem_classes="signup_form"):
            gr.Textbox(label="Username", placeholder="Enter your username", interactive=True)
            gr.Textbox(label="Password", placeholder="Enter your password", interactive=True)
            gr.Button("Sign Up")
