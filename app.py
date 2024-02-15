import cache
import flask

import resources
from routes import routing
from src import model
import login
import login.apps
import service
import species_trie.apps
from src import config

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = service.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.get_file_content(config.EnvKeys.FLASK_SECRET)
app.config["JWT_SECRET_KEY"] = config.get_file_content(config.EnvKeys.JWT_SECRET)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.get_jwt_access_token_expires()

app.config["CACHE_TYPE"] = config.get_cache_type()
app.config["CACHE_KEY_PREFIX"] = config.get_env(config.EnvKeys.CACHE_KEY_PREFIX)
app.config["CACHE_REDIS_HOST"] = config.get_env(config.EnvKeys.CACHE_REDIS_HOST)
app.config["CACHE_REDIS_PORT"] = config.get_env(config.EnvKeys.CACHE_REDIS_PORT)


resources.api.init_resources(routing.ROUTES)
resources.api.init_app(app)
login.jwt.init_app(app)
model.db.init_app(app)
model.migrate.init_app(app, model.db)
cache.cache.init_app(app)

app.register_blueprint(login.apps.blueprint)
app.register_blueprint(species_trie.apps.blueprint)

import cache.redis_client


@app.route("/keys")
def keys():
    return flask.jsonify([str(key) for key in cache.redis_client.client.keys()])


if __name__ == "__main__":

    cache.cache.clear()
    app.run(host="127.0.0.1", debug=True)
