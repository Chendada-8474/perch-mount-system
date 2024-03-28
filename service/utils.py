import os
import requests
import json
from src import config


END_POINT = f"{config.get_env(config.EnvKeys.FLEET_BEACON_HOST)}/delete_media"


def get_detected_medium(medium: dict) -> dict:
    id_field = (
        "empty_medium_id" if "empty_medium_id" in medium else "detected_medium_id"
    )
    return {"medium_id": medium[id_field], "path": medium["path"]}


def post_delete_media_task(task: list[str]):
    response = requests.post(END_POINT, data=json.dump(task))
    if not response.ok:
        raise SystemError("post delete media task failed")
