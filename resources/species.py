import flask

import resources
import service.species as ServiceSpecies


class Species(resources.PerchMountResource):
    def get(self):
        args = dict(flask.request.args)
        results = ServiceSpecies.get_species(**args)
        return {"species": [result.to_json() for result in results]}


class ASpecies(resources.PerchMountResource):
    def get(self, taxon_order: int):
        result = ServiceSpecies.get_species_by_taxon_order(taxon_order)
        return result.to_json()
