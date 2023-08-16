MEDIA_ROOT = "Z:/棲架資料庫"
HOST = "http://127.0.0.1:5000"
EMPTY_CHECK_LIMIT = 250
REVIEW_LIMIT = 100
IMAGE_EXTENSIONS = {"bmp", "jpg", "jpeg", "png", "tif", "tiff", "dng"}
VIDEO_EXTENSIONS = {"mov", "avi", "mp4", "mpg", "mpeg", "m4v", "wmv", "mkv"}
NUM_MEDIA_IN_PAGE = 50
TASKS_DIR_PATH = "D:/coding/demo_nas/task"

RAPTOR_ORDERS = {"Strigiformes", "Accipitriformes"}

cache = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
}
