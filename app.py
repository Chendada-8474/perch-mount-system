import cache
import flask
import flask_cors

import login
import login.apps
import login.utils
import resources
from resources.routes import routing
import service
import service.members
import species_trie.apps
import summary.apps
from src import model
from src import config

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = service.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.get_file_content(config.EnvKeys.FLASK_SECRET)
app.config["JWT_SECRET_KEY"] = config.get_file_content(config.EnvKeys.JWT_SECRET)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.get_jwt_access_token_expires()
# app.config["JWT_COOKIE_CSRF_PROTECT  "] = False
app.config["JWT_COOKIE_SAMESITE"] = "None"
app.config["JWT_CSRF_IN_COOKIES"] = True
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True

app.config["CACHE_TYPE"] = config.get_cache_type()
app.config["CACHE_KEY_PREFIX"] = config.get_env(config.EnvKeys.CACHE_KEY_PREFIX)
app.config["CACHE_REDIS_HOST"] = config.get_env(config.EnvKeys.CACHE_REDIS_HOST)
app.config["CACHE_REDIS_PORT"] = config.get_env(config.EnvKeys.CACHE_REDIS_PORT)


flask_cors.CORS(
    app,
    resources={
        r"/*": {"origins": config.get_env(config.EnvKeys.ACCESS_CCONTROL_ALLOW_ORIGIN)}
    },
    supports_credentials=True,
    allow_headers="*",
)
resources.api.init_resources(routing.ROUTES)
resources.api.init_app(app)
login.jwt.init_app(app)
model.db.init_app(app)
model.migrate.init_app(app, model.db)
cache.cache.init_app(app)


import cache.key
import cache.redis_client
import flask_jwt_extended


app.register_blueprint(login.apps.blueprint)
app.register_blueprint(species_trie.apps.blueprint)
app.register_blueprint(summary.apps.blueprint)


@app.route("/test/a/b/c")
def test():
    cache.key.evict_same_path_keys()
    return flask.request.root_path


@app.route("/keys")
@flask_jwt_extended.jwt_required()
def keys():
    return flask.jsonify([str(key) for key in cache.redis_client.client.keys()])


@app.after_request
def refresh_expiring_jwts(response: flask.Response):
    try:
        response.delete_cookie("access_token_cookie")
        token = login.utils.get_new_token_if_expired()
        if token:
            flask_jwt_extended.set_access_cookies(response, token)
        return response
    except (RuntimeError, KeyError):
        return response


if __name__ == "__main__":
    cache.cache.clear()
    app.run(host="127.0.0.1", debug=True)
