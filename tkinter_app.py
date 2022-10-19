import os
import tkinter.messagebox
from tkinter import *
from PIL import ImageTk, Image

from get_data import Slide

APP_BG_COLOR = "#6C8CD5"
FRAME_BG_COLOR = "#4671D5"
BOTTOM_BG_COLOR = "#06266F"
MODEL_NAME = ''
SLIDES = []
SLIDE_IDX = 0


def update_decorator(func, command_to_update):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    command_to_update()
    return wrapper


def set_root():
    main_window = Tk()
    main_window["bg"] = APP_BG_COLOR
    main_window.title("True Values Selector")
    main_window.geometry("1500x1200")
    main_window.resizable(width=True, height=True)
    main_window.minsize(width=1000, height=900)
    return main_window


def start_app(model_name, slides):
    root = set_root()
    show_app(root, model_name, slides)
    root.mainloop()


# not tkinter methods
def get_slide_text(slide: Slide):
    text = f"Slide idx: {SLIDE_IDX}/{len(SLIDES)}\n" \
           f"Video name: {slide.video_name}\n" \
           f"Frame num: {slide.frame}\n" \
           f"Selected true value: {slide.class_id} - {slide.class_name}\n" \
           f"{MODEL_NAME}'s prediction: ({', '.join(slide.prediction)})\n" \
           f"Video path: {slide.video_path}\n" \
           f"True values file path: {slide.true_values_file_path}"
    return text


def show_app(root, model_name, slides):
    global MODEL_NAME, SLIDES
    MODEL_NAME = model_name.capitalize()
    SLIDES = slides

    def main_app():

        def get_next():
            global SLIDE_IDX
            if SLIDE_IDX == len(SLIDES) - 1:
                tkinter.messagebox.showerror()
                return
            SLIDE_IDX += 1
            update_slide_info()

        def get_prev():
            global SLIDE_IDX
            if SLIDE_IDX == 0:
                tkinter.messagebox.showerror()
                return
            SLIDE_IDX -= 1
            update_slide_info()

        def update_slide_info():
            # updating info area
            slide_info.delete(1.0, 30.0)
            slide_info.insert(1.0, get_slide_text(SLIDES[SLIDE_IDX]))
            # updating selected_photo
            selected_img = get_selected_photo()
            selected_img_label = Label(top_left_frame, image=selected_img, bg=FRAME_BG_COLOR)
            selected_img_label.image = selected_img
            selected_img_label.place(relx=0.02, rely=0.02, relwidth=0.47, relheight=0.8)
            # updating selected_class_name
            selected_class = f"Selected: {SLIDES[SLIDE_IDX].class_id}"
            selected_var.set(selected_class)
            # updating predictions
            for i in range(1,4):
                pred_photo = get_pred_photo(i)
                pred_photo_label = Label(middle_frame, image=pred_photo, bg=FRAME_BG_COLOR)
                pred_photo_label.image = pred_photo
                if i==1:
                    pred_photo_label.place(relx = 0.02, rely=0.02, relwidth=0.31, relheight=0.8)
                elif i==2:
                    pred_photo_label.place(relx=0.35, rely=0.02, relwidth=0.31, relheight=0.8)
                else:
                    pred_photo_label.place(relx=0.68, rely=0.02, relwidth=0.31, relheight=0.8)
            # updating preds
            pred_1_class.set(SLIDES[SLIDE_IDX].prediction[0])
            pred_2_class.set(SLIDES[SLIDE_IDX].prediction[1])
            pred_3_class.set(SLIDES[SLIDE_IDX].prediction[2])


        def get_pred_photo(pred_number):
            photo_path = f"{os.path.join('all_classes_photos', f'{SLIDES[SLIDE_IDX].prediction[pred_number-1]}.png')}"
            if os.path.exists(photo_path):
                img = Image.open(photo_path)
                img = img.resize((416, 416))
                img = ImageTk.PhotoImage(img)
                return img
            return None
        def get_selected_photo():
            photo_path = f"{os.path.join('all_classes_photos', f'{SLIDES[SLIDE_IDX].class_id}.png')}"
            if os.path.exists(photo_path):
                img = Image.open(photo_path)
                img = img.resize((416, 416))
                img = ImageTk.PhotoImage(img)
                return img
            return None

        def hide_main_app():
            whole_frame.place_forget()
            start_frame.place(relwidth=1, relheight=1)

        start_frame.place_forget()

        whole_frame = Frame(root, bg=APP_BG_COLOR)
        whole_frame.place(relwidth=1, relheight=1)

        # main frames
        # top left frame area
        top_left_frame = Frame(whole_frame, bg=FRAME_BG_COLOR)
        top_left_frame.place(relx=0.03, rely=0.03, relwidth=0.6, relheight=0.43)
        # TODO: add video_photo
        selected_img = get_selected_photo()
        selected_img_label = Label(top_left_frame, image=selected_img, bg=FRAME_BG_COLOR)
        selected_img_label.image = selected_img
        selected_img_label.place(relx=0.02, rely=0.02, relwidth=0.47, relheight=0.8)
        selected_class = f"Selected: {SLIDES[SLIDE_IDX].class_id}"
        selected_var = StringVar(value=selected_class)
        selected_class_name = Label(top_left_frame, bg=FRAME_BG_COLOR, textvariable=selected_var)
        selected_class_name.place(relx=0.02, rely=0.84, relwidth=0.47, relheight=0.14)

        # top right frame area
        top_right_frame = Frame(whole_frame, bg=FRAME_BG_COLOR)
        top_right_frame.place(relx=0.66, rely=0.03, relwidth=0.31, relheight=0.43)

        slide_info = Text(top_right_frame, wrap=WORD)
        slide_info.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.96)
        slide_info.insert(1.0, get_slide_text(SLIDES[SLIDE_IDX]))

        # middle frame area
        middle_frame = Frame(whole_frame, bg=FRAME_BG_COLOR)
        middle_frame.place(relx=0.03, rely=0.5, relwidth=0.94, relheight=0.43)

        # pred 1
        pred_photo_1 = get_pred_photo(1)
        pred_photo_1_label = Label(middle_frame, image= pred_photo_1, bg=FRAME_BG_COLOR)
        pred_photo_1_label.image = selected_img
        pred_photo_1_label.place(relx = 0.02, rely=0.02, relwidth=0.31, relheight=0.8)
        pred_1_class = StringVar(value=f"{SLIDES[SLIDE_IDX].prediction[0]}")
        pred_photo_1_class_id = Label(middle_frame, textvariable=pred_1_class, bg=FRAME_BG_COLOR)
        pred_photo_1_class_id.place(relx=0.02, rely=0.84, relwidth=0.47, relheight=0.14)

        # pred 2
        pred_photo_2 = get_pred_photo(2)
        pred_photo_2_label = Label(middle_frame, image=pred_photo_2, bg=FRAME_BG_COLOR)
        pred_photo_2_label.image = selected_img
        pred_photo_2_label.place(relx=0.35, rely=0.02, relwidth=0.31, relheight=0.8)
        pred_2_class = StringVar(value=f"{SLIDES[SLIDE_IDX].prediction[1]}")
        pred_photo_2_class_id = Label(middle_frame, textvariable=pred_2_class, bg=FRAME_BG_COLOR)
        pred_photo_2_class_id.place(relx=0.35, rely=0.84, relwidth=0.47, relheight=0.14)
        # pred 3
        pred_photo_3 = get_pred_photo(3)
        pred_photo_3_label = Label(middle_frame, image=pred_photo_3, bg=FRAME_BG_COLOR)
        pred_photo_3_label.image = selected_img
        pred_photo_3_label.place(relx=0.68, rely=0.02, relwidth=0.31, relheight=0.8)
        pred_3_class = StringVar(value=f"{SLIDES[SLIDE_IDX].prediction[2]}")
        pred_photo_3_class_id = Label(middle_frame, textvariable=pred_3_class, bg=FRAME_BG_COLOR)
        pred_photo_3_class_id.place(relx=0.68, rely=0.84, relwidth=0.47, relheight=0.14)

        # bottom frame area
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
    model_name_label = Label(start_frame, text=f"Model name: {MODEL_NAME}", bg=APP_BG_COLOR)
    model_name_label.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.2)
