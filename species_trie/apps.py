import flask

from service import species
from species_trie import trie


trier = trie.SpeciesTrie(
    species.get_species(),
    species.get_species_codes(),
)

blueprint = flask.Blueprint("species_trie", __name__)


@blueprint.route("/trie")
def species_prediction():
    phrase = flask.request.args.get("phrase")
    return {"results": trier.search(phrase)}
