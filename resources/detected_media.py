import flask
from flask_restful import reqparse
import flask_jwt_extended

import cache
import cache.key
import resources
from resources import utils
import service.detected_media
import service.detected_individuals
import service.species
from src import config
from src import model

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

    @flask_jwt_extended.jwt_required()
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
        taxon_orders = utils.get_indiivduals_taxon_orders(individuals)
        species = service.species.get_species_by_taxon_orders(taxon_orders)
        species = utils.taxon_order_as_key(species)
        media = utils.custom_results_to_dict(media)
        media = utils.add_media_info(media)
        individuals = [individual.to_json() for individual in individuals]
        media_with_individuals = utils.embed_individuals_to_media(media, individuals)

        return {
            "media": media_with_individuals,
            "species": species,
        }

    @flask_jwt_extended.jwt_required()
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

    def _get_indiivduals_taxon_orders(
        self, individuals: list[model.DetectedIndividuals]
    ) -> list[int]:
        return [sp.taxon_order_by_ai for sp in individuals]


class DetectedMedium(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    def get(self, detected_medium_id: str):
        medium = service.detected_media.get_detected_medium_by_id(detected_medium_id)
        individuals = (
            service.detected_individuals.get_detected_individauls_by_medium_indice(
                [medium.detected_medium_id]
            )
        )

        taxon_orders = utils.get_indiivduals_taxon_orders(individuals)
        species = service.species.get_species_by_taxon_orders(taxon_orders)
        species = utils.taxon_order_as_key(species)
        medium = utils.to_dict(medium)
        medium = utils.add_medium_info(medium)
        medium["individuals"] = [individual.to_json() for individual in individuals]
        medium["species"] = species
        return medium
