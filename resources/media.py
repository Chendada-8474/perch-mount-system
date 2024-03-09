import flask
import flask_restful.reqparse
import flask_jwt_extended

import cache
import cache.key
import resources
from resources import utils
import service.media
import service.individuals
import service.species
from src import config

TIMEOUT = config.get_data_cache_timeout()


class Media(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("media", type=list[dict], required=True, location="json")
    put_parser = flask_restful.reqparse.RequestParser()
    put_parser.add_argument("media", type=list[dict], required=True, location="json")
    put_parser.add_argument(
        "detected_indices", type=list[str], required=True, location="json"
    )

    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(timeout=TIMEOUT, make_cache_key=cache.key.key_generate)
    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        media = service.media.get_media(**args)

        media_indice = [medium.medium_id for medium in media]
        individuals = service.individuals.get_individauls_by_medium_indice(media_indice)
        media = [medium.to_json() for medium in media]
        individuals = [individual.to_json() for individual in individuals]

        media_with_individuals = utils.embed_individuals_to_media(media, individuals)

        return {"media": media_with_individuals}

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        service.media.add_media_and_individuals(args["media"])
        cache.key.evict_same_path_keys()

    @flask_jwt_extended.jwt_required()
    def put(self):
        args = self.put_parser.parse_args(strict=True)
        service.media.review(args["detected_indices"], args["media"])
        cache.key.evict_same_path_keys()


class Medium(flask_restful.Resource):
    patch_parser = flask_restful.reqparse.RequestParser()
    patch_parser.add_argument("event", type=int)
    patch_parser.add_argument("featured", type=bool)
    patch_parser.add_argument("featured_by", type=int)
    patch_parser.add_argument("featured_behavior", type=int)
    patch_parser.add_argument("featured_title", type=str)

    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(timeout=TIMEOUT, make_cache_key=cache.key.key_generate)
    def get(self, medium_id: str):
        medium = service.media.get_medium_by_id(medium_id)
        individuals = service.individuals.get_individauls_by_medium_indice(
            [medium.medium_id]
        )
        taxon_orders = utils.get_indiivduals_taxon_orders(individuals)
        species = service.species.get_species_by_taxon_orders(taxon_orders)
        species = utils.taxon_order_as_key(species)
        individuals = [individual.to_json() for individual in individuals]
        medium = medium.to_json()
        medium["individuals"] = individuals
        medium["species"] = species
        return medium

    @flask_jwt_extended.jwt_required()
    def patch(self, medium_id: str):
        args = self.patch_parser.parse_args()
        service.media.update_medium(medium_id, args)
        medium = service.media.get_medium_by_id(medium_id)
        cache.key.evict_same_path_keys()
        return medium.to_json()
