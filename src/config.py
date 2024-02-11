import os
import json
import enum
import dotenv

dotenv.load_dotenv()

PREFIX = "PERCH_MOUNT"
IMAGE_EXTENSIONS = {"bmp", "jpg", "jpeg", "png", "tif", "tiff", "dng"}
VIDEO_EXTENSIONS = {"mov", "avi", "mp4", "mpg", "mpeg", "m4v", "wmv", "mkv"}
RAPTOR_ORDERS = {"Strigiformes", "Accipitriformes"}

class EnvKeys(enum.StrEnum):
    MEDIA_ROOT= enum.auto()
    TASKS_DIR_PATH= enum.auto()
    EMPTY_CHECK_LIMIT= enum.auto()
    REVIEW_LIMIT= enum.auto()
    DETECTED_EMPTY_CHECK_LIMIT= enum.auto()

    MINIO_HOST= enum.auto()
    MINIO_PORT= enum.auto()

    MYSQL_PASSWORD= enum.auto()
    MYSQL_USER= enum.auto()
    MYSQL_HOST= enum.auto()
    MYSQL_PORT= enum.auto()

def get_env(key: EnvKeys) -> str:
    return os.environ.get(f"{PREFIX}_{key.upper()}")

def get_file(key: EnvKeys) -> str:
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

# class General:
#     @staticmethod
#     def get_media_root() -> str:
#         return os.environ.get("MEDIA_ROOT")

#     @staticmethod
#     def get_tasks_dir_path() -> str:
#         return os.environ.get("TASKS_DIR_PATH")

#     @staticmethod
#     def get_empty_check_limit() -> str:
#         return os.environ.get("EMPTY_CHECK_LIMIT")

#     @staticmethod
#     def get_review_limit() -> str:
#         return os.environ.get("REVIEW_LIMIT")

#     @staticmethod
#     def get_detected_empty_check_limit() -> str:
#         return os.environ.get("DETECTED_EMPTY_CHECK_LIMIT")

#     @staticmethod
#     def get_image_extensions() -> set:
#         return set(json.loads(os.environ.get("IMAGE_EXTENSIONS")))

#     @staticmethod
#     def get_video_extensions() -> set:
#         return set(json.loads(os.environ.get("VIDEO_EXTENSIONS")))


# class Minio:
#     @staticmethod
#     def get_minio_host() -> str:
#         return os.environ.get("MINIO_HOST")

#     @staticmethod
#     def get_minio_port() -> str:
#         return os.environ.get("MINIO_PORT")


# class MySQL:
#     @staticmethod
#     def get_mysql_password() -> str:
#         return os.environ.get("MYSQL_PASSWORD")

#     @staticmethod
#     def get_mysql_user() -> str:
#         return os.environ.get("MYSQL_USER")

#     @staticmethod
#     def get_mysql_host() -> str:
#         return os.environ.get("MYSQL_HOST")

#     @staticmethod
#     def get_mysql_port() -> str:
#         return os.environ.get("MYSQL_PORT")

# if __name__ == "__main__":
#     e = get_env(EnvKeys.EMPTY_CHECK_LIMIT)
#     print(e)