from utils import evaluation_page, login_page


def main():
    """
    The main function of the program.
    :return: none
    """

    # Main app
    app = evaluation_page.app

    # Login page
    # app = login_page.app

    app.launch()


if __name__ == "__main__":
    main()
