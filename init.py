import os
import configs.config as config
import configs.path


def init_media_root():
    if not os.path.exists(configs.path.MEDIA_ROOT):
        os.makedirs(configs.path.MEDIA_ROOT)
    empty_dir = os.path.join(configs.path.MEDIA_ROOT, "空拍")
    if not os.path.exists(empty_dir):
        os.makedirs(empty_dir)


if __name__ == "__main__":
    init_media_root()
