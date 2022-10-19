import fire


def empty(*args, **kwargs):
    return


from get_data import get_data
from tkinter_app import start_app

if __name__ == "__main__":
    fire.core._PrintResult = empty
    model_name, slides = fire.Fire(get_data)
    start_app(model_name, slides)
