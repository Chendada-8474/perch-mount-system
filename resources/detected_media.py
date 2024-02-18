import flask
from flask_restful import reqparse

import cache
import cache.key
import resources
from resources import utils
import service.detected_media
import service.detected_individuals
from src import config

TIMEOUT = config.get_data_cache_timeout()


class DetectedMedia(resources.PerchMountResource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        "detected_media", type=list[dict], required=True, location="json"
    )
    put_parser = reqparse.RequestParser()
    put_parser.add_argument("section", type=dict, required=True, location="json")
    put_parser.add_argument(
        "detected_media", type=list[dict], required=True, location="json"
    )
    put_parser.add_argument(
        "empty_indices", type=list[str], required=True, location="json"
    )

    @cache.cache.cached(timeout=TIMEOUT, make_cache_key=cache.key.key_generate)
    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        media = service.detected_media.get_detected_media(**args)
        media_indice = [medium.detected_medium_id for medium in media]
        individuals = (
            service.detected_individuals.get_detected_individauls_by_medium_indice(
                media_indice
            )
        )
        media = [medium.to_json() for medium in media]
        individuals = [individual.to_json() for individual in individuals]
        media_with_individuals = utils.embed_individuals_to_media(media, individuals)

        return {"media": media_with_individuals}

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        service.detected_media.add_media_individuals(args["detected_media"])
        cache.key.evict_same_path_keys()

    def put(self):
        args = self.put_parser.parse_args(strict=True)
        service.detected_media.detect(
            args["section"],
            args["empty_indices"],
            args["detected_media"],
        )
        cache.key.evict_same_path_keys()
