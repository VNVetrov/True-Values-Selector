import tkinter.messagebox
from tkinter import *

APP_BG_COLOR = "#6C8CD5"
FRAME_BG_COLOR = "#4671D5"
BOTTOM_BG_COLOR = "#06266F"
MODEL_NAME = ''
SLIDES = []
SLIDE_IDX = 0


def get_next():
    global SLIDE_IDX
    if SLIDE_IDX == len(SLIDES) - 1:
        tkinter.messagebox.showerror()
        return
    SLIDE_IDX += 1


def get_prev():
    global SLIDE_IDX
    if SLIDE_IDX == 0:
        tkinter.messagebox.showerror()
        return
    SLIDE_IDX -= 1


def set_root():
    main_window = Tk()
    main_window["bg"] = APP_BG_COLOR
    main_window.title("True Values Selector")
    main_window.geometry("1400x900")
    main_window.resizable(width=True, height=True)
    main_window.minsize(width=1000, height=900)
    return main_window


def start_app(model_name, slides):
    root = set_root()
    show_app(root, model_name, slides)
    root.mainloop()


def show_app(root, model_name, slides):
    MODEL_NAME = model_name
    SLIDES = slides

    def main_app():

        def hide_main_app():
            whole_frame.place_forget()
            start_frame.place(relwidth=1, relheight=1)

        start_frame.place_forget()

        whole_frame = Frame(root, bg=APP_BG_COLOR)
        whole_frame.place(relwidth=1, relheight=1)

        # main frames
        top_left_frame = Frame(whole_frame, bg=FRAME_BG_COLOR)
        top_left_frame.place(relx=0.03, rely=0.03, relwidth=0.6, relheight=0.43)
        top_right_frame = Frame(whole_frame, bg=FRAME_BG_COLOR)
        top_right_frame.place(relx=0.66, rely=0.03, relwidth=0.31, relheight=0.43)
        middle_frame = Frame(whole_frame, bg=FRAME_BG_COLOR)
        middle_frame.place(relx=0.03, rely=0.5, relwidth=0.94, relheight=0.43)
        bottom_frame = Frame(whole_frame, bg=BOTTOM_BG_COLOR)
        bottom_frame.place(relx=0, rely=0.93, relwidth=1, relheight=0.7)

        next_button = Button(bottom_frame, text="Next", command=get_next)
        next_button.place(relx=0.85, rely=0.03, relwidth=0.1, relheight=0.05)
        prev_button = Button(bottom_frame, text="Prev", command=get_prev)
        prev_button.place(relx=0.7, rely=0.03, relwidth=0.1, relheight=0.05)
        back_to_menu_button = Button(bottom_frame, text="Menu", command=hide_main_app)
        back_to_menu_button.place(relx=0.05, rely=0.03, relwidth=0.1, relheight=0.05)

    start_frame = Frame(root, bg=APP_BG_COLOR)
    start_frame.place(relheight=1, relwidth=1)
    start_button = Button(start_frame, text="Start", command=main_app)
    start_button.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)
