import requests
import json
from src import config


END_POINT = f"{config.get_env(config.EnvKeys.FLEET_BEACON_HOST)}/delete_media"


def post_delete_media_task(task: list[str]):
    response = requests.post(END_POINT, data=json.dump(task))
    if not response.ok:
        raise SystemError("post delete media task failed")
