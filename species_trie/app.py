import flask
from service import species
from src import app
from tools.species_trie import trie


trier = trie.SpeciesTrie(
    species.get_species(),
    species.get_species_codes(),
)


@app.app.route("/species_prediction")
def species_prediction():
    phrase = flask.request.args.get("phrase")
    return {"results": trier.search(phrase)}
