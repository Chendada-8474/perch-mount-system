import os
import enum
from datetime import timedelta
import dotenv


dotenv.load_dotenv()

PREFIX = "PERCH_MOUNT"
IMAGE_EXTENSIONS = {"bmp", "jpg", "jpeg", "png", "tif", "tiff", "dng"}
VIDEO_EXTENSIONS = {"mov", "avi", "mp4", "mpg", "mpeg", "m4v", "wmv", "mkv"}
RAPTOR_ORDERS = {"Strigiformes", "Accipitriformes"}


class EnvKeys(enum.StrEnum):
    MEDIA_ROOT = enum.auto()
    TASKS_DIR_PATH = enum.auto()
    EMPTY_CHECK_LIMIT = enum.auto()
    REVIEW_LIMIT = enum.auto()
    DETECTED_EMPTY_CHECK_LIMIT = enum.auto()
    FLASK_SECRET = enum.auto()
    JWT_SECRET = enum.auto()

    MINIO_HOST = enum.auto()
    MINIO_PORT = enum.auto()

    MYSQL_PASSWORD = enum.auto()
    MYSQL_USER = enum.auto()
    MYSQL_HOST = enum.auto()
    MYSQL_PORT = enum.auto()

    CACHE_REDIS_HOST = enum.auto()
    CACHE_REDIS_PORT = enum.auto()


def get_env(key: EnvKeys) -> str:
    return os.environ.get(f"{PREFIX}_{key.upper()}")


def get_file_content(key: EnvKeys) -> str:
    path = get_env(key)
    with open(path) as file:
        content = file.readline()
    return content


def get_image_extensions() -> set:
    return IMAGE_EXTENSIONS


def get_vedio_extenstions() -> set:
    return VIDEO_EXTENSIONS


def get_raptor_orders() -> set:
    return RAPTOR_ORDERS


def get_jwt_access_token_expires() -> timedelta:
    return timedelta(weeks=7)


def get_jwt_refresh_expires() -> timedelta:
    return timedelta(days=1)
