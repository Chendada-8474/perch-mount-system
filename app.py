from datetime import datetime, timezone, timedelta
import flask
import flask_jwt_extended
import http

from src.routes import route_helper
from src.routes import routing
import service
from src import model
from src import config
from login import authenticate

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = service.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.get_file_content(config.EnvKeys.FLASK_SECRET)
app.config["JWT_SECRET_KEY"] = config.get_file_content(config.EnvKeys.JWT_SECRET)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.get_jwt_access_token_expires()

api = route_helper.PerchMountApi(app)
api.init_resources(routing.ROUTES)
jwt = flask_jwt_extended.JWTManager(app)

model.db.init_app(app)
model.migrate.init_app(app, model.db)


@app.route("/login", methods=["POST"])
def login():
    username = flask.request.json.get("username", None)
    phone_number = flask.request.json.get("phone_number", None)
    login_user = authenticate.get_user_if_autherized(username, phone_number)
    if not login_user:
        return (
            flask.jsonify({"message": "Bad username or password"}),
            http.HTTPStatus.UNAUTHORIZED,
        )
    additional_claims = {
        "is_admin": login_user.is_admin,
        "is_super_admin": login_user.is_super_admin,
    }
    access_token = flask_jwt_extended.create_access_token(
        identity=username,
        additional_claims=additional_claims,
    )
    return flask.jsonify(access_token=access_token)


@app.route("/logout", methods=["POST"])
def logout():
    response = flask.jsonify({"msg": "logout successful"})
    flask_jwt_extended.unset_jwt_cookies(response)
    return response


@app.after_request
def refresh_expiring_jwts(response: flask.Response):
    try:
        response.delete_cookie("access_token_cookie")
        exp_timestamp = flask_jwt_extended.get_jwt()["exp"]
        now = datetime.now(timezone(timedelta(hours=8)))
        target_timestamp = datetime.timestamp(now + config.get_jwt_refresh_expires())
        if target_timestamp > exp_timestamp:
            access_token = flask_jwt_extended.create_access_token(
                identity=flask_jwt_extended.get_jwt_identity()
            )
            flask_jwt_extended.set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@app.route("/test", methods=["GET"])
@flask_jwt_extended.jwt_required()
def test():
    current_user = flask_jwt_extended.get_jwt_identity()
    claims = flask_jwt_extended.get_jwt()
    return flask.jsonify({"user": current_user, "claims": claims})


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
