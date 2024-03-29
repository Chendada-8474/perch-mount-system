import flask
import flask_cors
import cache
import cache.key
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
app.config["PROPAGATE_EXCEPTIONS"] = True
# app.config["JWT_COOKIE_SAMESITE"] = "None"
# app.config["JWT_CSRF_IN_COOKIES"] = True
# app.config["JWT_CSRF_METHODS"] = []
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
# app.config["JWT_COOKIE_SECURE"] = True
# app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
# app.config["JWT_REFRESH_COOKIE_PATH"] = "/"

app.config["CACHE_TYPE"] = config.get_cache_type()
app.config["CACHE_KEY_PREFIX"] = config.get_env(config.EnvKeys.CACHE_KEY_PREFIX)
app.config["CACHE_REDIS_HOST"] = config.get_env(config.EnvKeys.CACHE_REDIS_HOST)
app.config["CACHE_REDIS_PORT"] = config.get_env(config.EnvKeys.CACHE_REDIS_PORT)


flask_cors.CORS(
    app,
    resources={
        r"/*": {"origins": config.get_env(config.EnvKeys.ACCESS_CONTROL_ALLOW_ORIGIN)}
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

app.register_blueprint(login.apps.blueprint)
app.register_blueprint(species_trie.apps.blueprint)
app.register_blueprint(summary.apps.blueprint)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/_clear_cache/<string:group>")
def clear_cache(group: str):
    cache.key.evict_group_cache(group)


# @app.after_request
# def refresh_expiring_jwts(response: flask.Response):
#     try:
#         response.delete_cookie("access_token_cookie")
#         token = login.utils.get_new_token_if_expired()
#         if token:
#             flask_jwt_extended.set_access_cookies(response, token)
#         return response
#     except (RuntimeError, KeyError):
#         return response


if __name__ == "__main__":
    cache.cache.clear()
    app.run(host="127.0.0.1", debug=True)
