import datetime
import json
import os.path
import shutil
import tkinter.messagebox
from json import JSONDecodeError


def make_backup(true_values_dir: str):
    true_values_dir = os.path.normpath(true_values_dir)
    backup_dir = true_values_dir + "_backup_" + datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
        shutil.copytree(src=true_values_dir, dst=backup_dir, dirs_exist_ok=True)
        tkinter.messagebox.showinfo("Success!", f"Backup files at {backup_dir}")
    else:
        tkinter.messagebox.showinfo("Sorry!", "You can create backup in 1 minute!")


def add_changes(slide_idx, slide, new_class):
    changes = {
        "SLIDE_IDX": slide_idx,
        "changed_to": new_class
    }
    slide_dict = {f"{name}": value for name, value in slide.__dict__.items() if not name.startswith("__")}
    changes = dict(**changes, **slide_dict)
    # all_changes = []
    if not os.path.exists('changes.json'):
        f = open('changes.json', 'w')
        f.close()
    #         json.dump(obj=all_changes, fp=f1)
    with open("changes.json", 'r+') as f:
        try:
            file = json.load(f)
        except JSONDecodeError:
            file = []
        flag = False
        for change in file:
            if change['video_name'] == slide.video_name and change['frame'] == slide.frame:
                flag = True
                tkinter.messagebox.showinfo("Be careful!",
                                            f"You have previously changed class {change['class_id']} "
                                            f"to {change['changed_to']} in video {slide.video_name} at {slide.frame}"
                                            f" frame. Now you want to change it to {changes['changed_to']}. "
                                            f"If you want to change your opinion, delete SLIDE_IDX {slide_idx} from "
                                            f"changes.json")
        if not flag:
            file.append(changes)
    with open('changes.json', 'w') as f2:
        json.dump(fp=f2, obj=file)


def make_migration():
    if os.path.exists('changes.json'):
        print(f"Migrations: {datetime.datetime.now().strftime('%d-%m-%Y_%H-%M')}")
        with open('changes.json', 'r') as f:
            migrations = json.load(f)
        for migration in migrations:
            true_values_slide_dir = migration['true_values_file_path']
            frame = migration['frame']
            new_class = migration['changed_to']
            with open(true_values_slide_dir, 'r') as f:
                file = f.readlines()
            new_file = []
            for line in file:
                # ignore commented lines
                if line.startswith("#"):
                    new_file.append(line)
                elems = line.split("-")
                elems = [elem.strip() for elem in elems]
                value = {
                    "from": int(elems[0]),
                    "to": int(elems[1]),
                    "class": elems[2]
                }
                if value['from'] <= frame <= value['to']:
                    new_file.append(f"{value['from']} - {value['to']} - {new_class}")
                else:
                    new_file.append(line)
            with open(true_values_slide_dir, 'w') as f:
                f.writelines(new_file)
            print(f"You have changed: {true_values_slide_dir}")
    else:
        tkinter.messagebox.showinfo("Sorry!", "You cannot make migration now, because config.json does not exist")
