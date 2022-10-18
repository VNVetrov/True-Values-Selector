import json
import re

from tkinter_app import start_app


class Slide:
    def __init__(self, video_name, video_path, true_values_file_path, frame, class_id, class_name, prediction):
        self.video_name = video_name
        self.video_path = video_path
        self.true_values_file_path = true_values_file_path
        self.frame = frame
        self.class_id = class_id
        self.class_name = class_name
        self.prediction = prediction


def read_json(json_path):
    with open(json_path, 'r') as f:
        file = json.load(f)
    return file


def get_tuple_of_pred(pred_string):
    regex = r"[0-9]{4}"
    matches = re.findall(regex, pred_string, re.MULTILINE)
    return tuple(matches)


def get_slides_data(json_path):
    data_dict = read_json(json_path)
    slides = []
    model_name = data_dict['model_name']
    for video in data_dict['results']:
        for prediction in video['predictions']:
            if not prediction['correct']:
                slide = Slide(video_name=video['video_name'],
                              video_path=video['video_path'],
                              true_values_file_path=video['true_values_file_path'],
                              frame=prediction['frame'],
                              class_id=prediction['class_id'],
                              class_name=prediction['class_name'],
                              prediction=get_tuple_of_pred(prediction['pred_variants']))
                slides.append(slide)
    return model_name, slides


def get_data(
        json_path: str = '',
        photos_path: str = '',
        true_values_dir: str = ''
):
    # if not os.path.isfile(json_path):
    #     print("Wrong json_path")
    #     return
    # if not os.path.isdir(photos_path) or not os.path.isdir(true_values_dir):
    #     print("Wrong photos_path or true_values_dir")
    #     return
    model_name, slides = get_slides_data(json_path)

    start_app(model_name, slides)
