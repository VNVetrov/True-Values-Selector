import os
from math import factorial
from tkinter import messagebox
from tkinter import *
from typing import Any
from PIL import ImageTk, Image
from enum import Enum


# enum
class RbStatus(Enum):
    permutations_no_repeat = 0
    placements_no_repeat = 1
    combinations_no_repeat = 2
    permutations_repeat = 3
    placements_repeat = 4
    combinations_repeat = 5


def is_with_repeat(num):
    return num > 2


# calculating functions
def calculate_permutations(n: int, k: int, rb_status: int) -> float:
    if is_with_repeat(rb_status):
        result = n ** n
    else:
        result = factorial(n)
    return result


def calculate_placements(n: int, k: int, rb_status: int) -> float:
    if is_with_repeat(rb_status):
        result = n ** k
    else:
        result = factorial(n) / factorial(n - k)
    return result


def calculate_combinations(n: int, k: int, rb_status: int) -> float:
    if is_with_repeat(rb_status):
        result = factorial(n + k - 1) / (factorial(n - 1) * factorial(k))
    else:
        result = factorial(n) / (factorial(n - k) * factorial(k))
    return result


# change this param to scale all sizes
MULTIPLIER = 1.6

# common params
FONT_COLOR = "#bdc1c6"
FRAME_BG_COLOR = "#171717"
ROOT_BG_COLOR = "#202124"
INPUT_COLOR = "#303134"
FONT_SIZE = 15 * MULTIPLIER
FONT_PARAM = ('Roboto Thin', int(FONT_SIZE), "bold")
CURSOR = "hand2"
INSERT_COLOR = "red"

# structured data
IMAGES_PATH_DICT = {
    RbStatus.permutations_no_repeat.value: f"{os.path.join('imgs', 'per_nr.png')}",
    RbStatus.placements_no_repeat.value: f"{os.path.join('imgs', 'pla_nr.png')}",
    RbStatus.combinations_no_repeat.value: f"{os.path.join('imgs', 'com_nr.png')}",
    RbStatus.permutations_repeat.value: f"{os.path.join('imgs', 'per_r.png')}",
    RbStatus.placements_repeat.value: f"{os.path.join('imgs', 'pla_r.png')}",
    RbStatus.combinations_repeat.value: f"{os.path.join('imgs', 'com_r.png')}"
}

CALCULATE_FUNC_DICT = {
    RbStatus.permutations_no_repeat.value: calculate_permutations,
    RbStatus.placements_no_repeat.value: calculate_placements,
    RbStatus.combinations_no_repeat.value: calculate_combinations,
    RbStatus.permutations_repeat.value: calculate_permutations,
    RbStatus.placements_repeat.value: calculate_placements,
    RbStatus.combinations_repeat.value: calculate_combinations
}


def get_image_depend_on_rb(rb_status, zone):
    img = Image.open(IMAGES_PATH_DICT[rb_status])
    img = img.resize((int(100 * MULTIPLIER), int(90 * MULTIPLIER)))
    img = ImageTk.PhotoImage(img)
    label = Label(zone, image=img)
    label.image = img
    return label


def check_for_mistakes(n, k, rb_status):
    n, k = n.strip(), k.strip()
    error_message = "Введите "
    is_error = False
    if not n.isdigit() and n:
        error_message += "N"
        is_error = True
    if not k.isdigit() and k:
        if rb_status not in (0, 3):
            if is_error:
                error_message += " и K"
            else:
                error_message += "K"
        is_error = True

    error_message += " заново!"
    if is_error:
        messagebox.showerror("Неверный ввод!", error_message)
    return is_error


def calculate_result(n, k, rb_status):
    return CALCULATE_FUNC_DICT[rb_status](n, k, rb_status)


def show_app(main_window: Any = None):
    # inner functions

    def set_img():
        rb_status = (rb_var.get() + 3) if repeat_var.get() else rb_var.get()
        image_formula_label = get_image_depend_on_rb(
            rb_status,
            zone=bottom_left_frame)
        image_formula_label.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.3)
        if rb_status in (0, 3):
            k_input.configure(state="disabled")
        else:
            k_input.configure(state="normal")

    def set_output():
        n = n_var.get()
        k = k_var.get()
        rb_status = (rb_var.get() + 3) if repeat_var.get() else rb_var.get()
        if check_for_mistakes(n, k, rb_status):
            return
        if not n:
            return
        n = int(n)
        if rb_status not in (0, 3):
            k = int(k)
            if rb_status in (1, 2) and k > n:
                messagebox.showerror("Неверный ввод!", "В данном случае K не может быть больше N!")
                return

        result = calculate_result(n, k, rb_status)
        output_var.set(int(float(result)))

    # frames
    top_left_frame = Frame(main_window, bg=FRAME_BG_COLOR)
    top_left_frame.place(relx=0.05, rely=0.05, relwidth=0.45, relheight=0.35)
    top_right_frame = Frame(main_window, bg=FRAME_BG_COLOR)
    top_right_frame.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.35)
    center_frame = Frame(main_window, bg=FRAME_BG_COLOR)
    center_frame.place(relx=0.05, rely=0.45, relwidth=0.9, relheight=0.24)
    bottom_left_frame = Frame(main_window, bg=FRAME_BG_COLOR)
    bottom_left_frame.place(relx=0.05, rely=0.74, relwidth=0.45, relheight=0.23)
    bottom_right_frame = Frame(main_window, bg=FRAME_BG_COLOR)
    bottom_right_frame.place(relx=0.55, rely=0.74, relwidth=0.4, relheight=0.23)

    # permutations, placements, combinations radiobuttons zone
    rb_var = IntVar()

    rb_permutations = Radiobutton(top_left_frame, text="Перестановки", variable=rb_var, value=0,
                                  bg=FRAME_BG_COLOR, font=FONT_PARAM, fg=FONT_COLOR, selectcolor=FRAME_BG_COLOR,
                                  activebackground=FRAME_BG_COLOR, activeforeground=FONT_COLOR, command=set_img)
    rb_permutations.place(relx=0.15, rely=0.2, relwidth=0.7, relheight=0.2)

    rb_placements = Radiobutton(top_left_frame, text="Размещения", variable=rb_var, value=1, bg=FRAME_BG_COLOR,
                                font=FONT_PARAM, fg=FONT_COLOR, selectcolor=FRAME_BG_COLOR,
                                activebackground=FRAME_BG_COLOR, activeforeground=FONT_COLOR, command=set_img)
    rb_placements.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.2)

    rb_combinations = Radiobutton(top_left_frame, text="Сочетания", variable=rb_var, value=2, bg=FRAME_BG_COLOR,
                                  font=FONT_PARAM, fg=FONT_COLOR, selectcolor=FRAME_BG_COLOR,
                                  activebackground=FRAME_BG_COLOR, activeforeground=FONT_COLOR, command=set_img)
    rb_combinations.place(relx=0.15, rely=0.6, relwidth=0.7)

    # is_with_repeat zone
    repeat_var = IntVar()

    cb_is_repeat = Checkbutton(top_right_frame, text="С повторениями", variable=repeat_var,
                               bg=FRAME_BG_COLOR, fg=FONT_COLOR, font=FONT_PARAM, selectcolor=FRAME_BG_COLOR,
                               activebackground=FRAME_BG_COLOR, activeforeground=FONT_COLOR, command=set_img,
                               onvalue=True, offvalue=False)
    cb_is_repeat.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    # result output label zone

    result_label = Label(bottom_right_frame, text="Результат: ", bg=FRAME_BG_COLOR, fg=FONT_COLOR, font=FONT_PARAM)
    result_label.place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.6)

    output_var = StringVar()
    output_string = Label(bottom_right_frame, textvariable=output_var, bg=FRAME_BG_COLOR, fg=FONT_COLOR,
                          font=FONT_PARAM, anchor='w', wraplength=int(147 * MULTIPLIER))
    output_string.place(relx=0.43, rely=0.2, relwidth=0.55, relheight=0.6)

    # button zone
    button_solve = Button(bottom_left_frame, text="Вычислить", fg=FONT_COLOR, bg=FRAME_BG_COLOR, font=FONT_PARAM,
                          activeforeground=FONT_COLOR, activebackground=FRAME_BG_COLOR, borderwidth=4, relief="ridge",
                          command=set_output)
    button_solve.place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.6)

    # center labels and entries zone
    n_var = StringVar()
    n_input = Entry(center_frame, bg='white', font=FONT_PARAM, background=INPUT_COLOR, borderwidth=0, fg=FONT_COLOR,
                    justify="center", disabledbackground="black", cursor=CURSOR, insertbackground=INSERT_COLOR,
                    selectbackground=FRAME_BG_COLOR, textvariable=n_var)
    n_input.place(relx=0.15, rely=0.33, relwidth=0.3, relheight=0.3)
    k_var = StringVar()
    k_input = Entry(center_frame, bg='white', font=FONT_PARAM, background=INPUT_COLOR, borderwidth=0, fg=FONT_COLOR,
                    justify="center", disabledbackground="black", cursor=CURSOR, insertbackground=INSERT_COLOR,
                    selectbackground=FRAME_BG_COLOR, textvariable=k_var)
    k_input.place(relx=0.65, rely=0.33, relwidth=0.3, relheight=0.3)

    n_text_label = Label(center_frame, text="N =", font=FONT_PARAM, bg=FRAME_BG_COLOR, fg=FONT_COLOR)
    n_text_label.place(relx=0.05, rely=0.33, relwidth=0.1, relheight=0.28)

    k_text_label = Label(center_frame, text="K =", font=FONT_PARAM, bg=FRAME_BG_COLOR, fg=FONT_COLOR)
    k_text_label.place(relx=0.55, rely=0.33, relwidth=0.1, relheight=0.28)

    # set img for first time
    set_img()


def set_root():
    main_window = Tk()
    main_window["bg"] = ROOT_BG_COLOR
    main_window.title("Помогатор ТерВер")
    main_window.geometry(f"{int(700 * MULTIPLIER)}x{int(450 * MULTIPLIER)}")
    main_window.resizable(width=False, height=False)
    main_window.iconbitmap("favicon.ico")
    return main_window


if __name__ == '__main__':
    root = set_root()
    show_app(root)
    root.mainloop()
