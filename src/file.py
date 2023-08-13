import os
import sys
from datetime import datetime
from cryptography.fernet import Fernet

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import configs.config as config


class Encryptor:
    _key = Fernet.generate_key()

    def encrypt(self, pwd):
        cipher_suite = Fernet(self._key)
        bpwd = bytes(pwd, "utf-8")
        ciphered_text = cipher_suite.encrypt(bpwd)
        return ciphered_text

    def decrypt(self, enc_pwd):
        cipher_suite = Fernet(self._key)
        uncipher_text = cipher_suite.decrypt(enc_pwd)
        return bytes(uncipher_text).decode("utf-8")


def move_to_empty(path: str):
    file_name = os.path.basename(path)
    date_str = datetime.now().strftime("%Y-%m-%d")
    dir_path = os.path.join(config.MEDIA_ROOT, "空拍", date_str)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    os.rename(path, os.path.join(dir_path, file_name))


def add_all_is_image(media: list[dict]):
    for medium in media:
        if medium["path"]:
            _, ext = os.path.splitext(medium["path"])
            ext = ext[1:].lower()
            medium["is_image"] = ext in config.IMAGE_EXTENSIONS
        else:
            medium["is_image"] = None
    return media


def add_is_image(medium: dict):
    if medium["path"]:
        _, ext = os.path.splitext(medium["path"])
        ext = ext[1:].lower()
        medium["is_image"] = ext in config.IMAGE_EXTENSIONS
    else:
        medium["is_image"] = None
    return medium


def add_all_file_name(media: list[dict]):
    for medium in media:
        medium["file_name"] = (
            os.path.basename(medium["path"]) if medium["path"] else None
        )
    return media


def add_file_name(medium: dict):
    medium["file_name"] = os.path.basename(medium["path"]) if medium["path"] else None
    return medium


if __name__ == "__main__":
    e = Encryptor()
    path = "s測試"
