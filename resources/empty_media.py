import flask
import flask_restful.reqparse
import flask_jwt_extended

import cache
import cache.key
import service.empty_media
from src import config
import resources
import resources.utils

TIMEOUT = config.get_data_cache_timeout()


class EmptyMedia(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("media", type=list[dict], required=True, location="json")
    put_parser = flask_restful.reqparse.RequestParser()
    put_parser.add_argument("media", type=list[dict], required=True, location="json")

    @flask_jwt_extended.jwt_required()
    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        media = service.empty_media.get_empty_media(**args)
        media = resources.utils.custom_results_to_dict(media)
        media = resources.utils.add_media_info(media)
        return {"media": media}

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        service.empty_media.add_empty_media(args["media"])
        cache.key.evict_same_path_keys()
        return {"message": "success"}

    @flask_jwt_extended.jwt_required()
    def put(self):
        args = self.put_parser.parse_args(strict=True)
        service.empty_media.empty_check(args.media)


class emptyMedium(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    def get(self, empty_medium_id: str):
        medium = service.empty_media.get_empty_medium_by_id(empty_medium_id)
        medium = resources.utils.to_dict(medium)
        medium = resources.utils.add_medium_info(medium)
        return medium
