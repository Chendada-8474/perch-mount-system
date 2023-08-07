import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import configs.config as config


def move_to_empty(path: str):
    file_name = os.path.basename(path)
    date_str = datetime.now().strftime("%Y-%m-%d")
    dir_path = os.path.join(config.MEDIA_ROOT, "空拍", date_str)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    os.rename(path, os.path.join(dir_path, file_name))


def add_is_image(media: list[dict]):
    for medium in media:
        _, ext = os.path.splitext(medium["path"])
        ext = ext[1:].lower()
        medium["is_image"] = ext in config.IMAGE_EXTENSIONS
    return media


def add_file_name(media: list[dict]):
    for medium in media:
        medium["file_name"] = os.path.basename(medium["path"])
    return media
