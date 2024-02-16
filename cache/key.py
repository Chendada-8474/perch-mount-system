import flask

import cache.pathlib
import cache.redis_client
from src import config


def key_generate(*_, **__) -> str:
    args = flask.request.args
    return phrase_key(args)


def phrase_key(args: dict) -> str:
    args_list = [f"{k}={v}" for k, v in args.items()]
    args_list.sort()
    key = "&".join(args_list)
    return f"{flask.request.path}?{key}" if key else flask.request.path


def group_of_key(key: str) -> str:
    return key.split("?")[0]


def evict_same_path_keys():
    prefix = config.get_env(config.EnvKeys.CACHE_KEY_PREFIX)
    path = cache.pathlib.CachePath(flask.request.path)
    group = path.ancestor.as_posix()
    for key in cache.redis_client.client.scan_iter(f"{prefix}{group}*"):
        cache.redis_client.client.delete(key)
