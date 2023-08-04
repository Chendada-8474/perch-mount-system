import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import configs.config as config


def move_to_empty(path: str):
    file_name = os.path.basename(path)
    date_str = datetime.now().strftime("%Y-%m-%d")
    dir_path = os.path.join(config.MEDIA_ROOT, date_str)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    os.rename(path, os.path.join(config.MEDIA_ROOT, date_str, file_name))


if __name__ == "__main__":
    path = "D:/coding/python/perch_mount_system/demo_media/06230559.JPG"
    move_to_empty(path)
