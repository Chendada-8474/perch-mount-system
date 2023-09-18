HOST = "http://127.0.0.1:5000"
EMPTY_CHECK_LIMIT = 250
REVIEW_LIMIT = 100
DETECTED_EMPTY_CHECK_LIMIT = 250
NUM_MEDIA_IN_PAGE = 50

IMAGE_EXTENSIONS = {"bmp", "jpg", "jpeg", "png", "tif", "tiff", "dng"}
VIDEO_EXTENSIONS = {"mov", "avi", "mp4", "mpg", "mpeg", "m4v", "wmv", "mkv"}

RAPTOR_ORDERS = {"Strigiformes", "Accipitriformes"}

cache = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
}


PROCESSED_DATA_REMAIN_DAYS = 7
