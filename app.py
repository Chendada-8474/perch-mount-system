import cache
import resources
from routes import routing
from src import model
from src import app
import login
import login.apps
import species_trie.apps

resources.api.init_resources(routing.ROUTES)
resources.api.init_app(app.app)
login.jwt.init_app(app.app)
model.db.init_app(app.app)
model.migrate.init_app(app.app, model.db)
cache.cache.init_app(app.app)


@app.app.route("/keys")
def keys():
    return "hi"


if __name__ == "__main__":
    app.app.run(host="127.0.0.1", debug=True)
