import os
import configs.config as config


def init_media_root():
    if not os.path.exists(config.MEDIA_ROOT):
        os.makedirs(config.MEDIA_ROOT)


if __name__ == "__main__":
    init_media_root()
