import os
import configs.config as config


def init_media_root():
    if not os.path.exists(config.MEDIA_ROOT):
        os.makedirs(config.MEDIA_ROOT)
    empty_dir = os.path.join(config.MEDIA_ROOT, "空拍")
    if not os.path.exists(empty_dir):
        os.makedirs(empty_dir)


if __name__ == "__main__":
    init_media_root()
