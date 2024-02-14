import flask
import http

from service import species
from src import app
from species_trie import trie


trier = trie.SpeciesTrie(
    species.get_species(),
    species.get_species_codes(),
)


@app.app.route("/species_prediction", methods=[http.HTTPMethod.GET])
def species_prediction():
    phrase = flask.request.args.get("phrase")
    return {"results": trier.search(phrase)}
