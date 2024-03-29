import flask

import cache
import cache.key
import resources
import service.species


class Species(resources.PerchMountResource):
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        args = dict(flask.request.args)
        results = service.species.get_species(**args)
        return {"species": [result.to_json() for result in results]}


class ASpecies(resources.PerchMountResource):
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self, taxon_order: int):
        result = service.species.get_species_by_taxon_order(taxon_order)
        return result.to_json()
