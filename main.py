import fire

from get_data import get_data
from tkinter_app import start_app


def empty(*args, **kwargs):
    return


if __name__ == "__main__":
    fire.core._PrintResult = empty
    model_name, slides, photos_path = fire.Fire(get_data)
    start_app(model_name, slides, photos_path)
