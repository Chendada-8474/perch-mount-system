import flask
import resources
import flask_restful.reqparse

import cache
import cache.key

import service.empty_media
from src import config

TIMEOUT = config.get_data_cache_timeout()


class EmptyMedia(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("media", type=list[dict], required=True, location="json")

    # @cache.cache.cached(timeout=TIMEOUT, make_cache_key=cache.key.key_generate)
    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        media = service.empty_media.get_empty_media(**args)
        return {"media": [medium.to_json() for medium in media]}

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        service.empty_media.add_empty_media(args["media"])
        cache.key.evict_same_path_keys()
        return {"message": "success"}
