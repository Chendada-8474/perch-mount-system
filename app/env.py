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
    ACCESS_CONTROL_ALLOW_ORIGIN = enum.auto()
    FLASK_SECRET = enum.auto()
    JWT_SECRET = enum.auto()

    FIRST_USER_GMAIL = enum.auto()
    FIRST_USER_FIRST_NAME = enum.auto()
    FIRST_USER_LAST_NAME = enum.auto()

    MINIO = enum.auto()
    MINIO_HTTPS_HOST = enum.auto()
    MINIO_BUCKET = enum.auto()
    MINIO_ACCESS_KEY = enum.auto()
    MINIO_SECRET_KEY = enum.auto()
    MINIO_DATA_EXPORT_BUCKET = enum.auto()

    POSTGRESQL_PASSWORD = enum.auto()
    POSTGRESQL_USER = enum.auto()
    POSTGRESQL_HOST = enum.auto()
    POSTGRESQL_PORT = enum.auto()
    POSTGRESQL_DATABASE_NAME = enum.auto()

    CACHE_DEFAULT_TIMEOUT = enum.auto()
    CACHE_KEY_PREFIX = enum.auto()
    CACHE_REDIS_HOST = enum.auto()
    CACHE_REDIS_PORT = enum.auto()
    REDIS_MAXMEMORY = enum.auto()
    REDIS_MAXMEMORY_POLICY = enum.auto()

    FLEET_BEACON_HOST = enum.auto()

    EXPORT_DATA_RETAIN_DAYS = enum.auto()

    GOOGLE_OAUTH2_CLIENT_ID = enum.auto()


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
    # return timedelta(hours=1)
    return timedelta(days=30)


def get_jwt_refresh_expires() -> timedelta:
    # return timedelta(seconds=3599)
    return timedelta(days=1)


def get_cache_type() -> str:
    return "RedisCache"


def get_data_cache_timeout() -> int:
    return 3600
