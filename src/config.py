import os
import json
from dotenv import load_dotenv

load_dotenv()


class General:
    @staticmethod
    def get_media_root() -> str:
        return os.environ.get("MEDIA_ROOT")

    @staticmethod
    def get_tasks_dir_path() -> str:
        return os.environ.get("TASKS_DIR_PATH")

    @staticmethod
    def get_empty_check_limit() -> str:
        return os.environ.get("EMPTY_CHECK_LIMIT")

    @staticmethod
    def get_review_limit() -> str:
        return os.environ.get("REVIEW_LIMIT")

    @staticmethod
    def get_detected_empty_check_limit() -> str:
        return os.environ.get("DETECTED_EMPTY_CHECK_LIMIT")

    @staticmethod
    def get_image_extensions() -> set:
        return set(json.loads(os.environ.get("IMAGE_EXTENSIONS")))

    @staticmethod
    def get_video_extensions() -> set:
        return set(json.loads(os.environ.get("VIDEO_EXTENSIONS")))


class Minio:
    @staticmethod
    def get_minio_host() -> str:
        return os.environ.get("MINIO_HOST")

    @staticmethod
    def get_minio_port() -> str:
        return os.environ.get("MINIO_PORT")


class MySQL:
    @staticmethod
    def get_mysql_password() -> str:
        return os.environ.get("MYSQL_PASSWORD")

    @staticmethod
    def get_mysql_user() -> str:
        return os.environ.get("MYSQL_USER")

    @staticmethod
    def get_mysql_host() -> str:
        return os.environ.get("MYSQL_HOST")

    @staticmethod
    def get_mysql_port() -> str:
        return os.environ.get("MYSQL_PORT")
