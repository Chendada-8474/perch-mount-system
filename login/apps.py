import flask
import flask_jwt_extended
import http

from login import authenticate
from login import utils

blueprint = flask.Blueprint("login", __name__)


@blueprint.route("/login", methods=[http.HTTPMethod.POST])
def login():
    username = flask.request.json.get("username", None)
    phone_number = flask.request.json.get("phone_number", None)
    login_user = authenticate.get_user_if_autherized(username, phone_number)
    if not login_user:
        return (
            flask.jsonify({"message": "Bad username or password"}),
            http.HTTPStatus.UNAUTHORIZED,
        )
    additional_claims = utils.get_authorization_claims(login_user)
    access_token = flask_jwt_extended.create_access_token(
        identity=username,
        additional_claims=additional_claims,
    )
    return flask.jsonify(access_token=access_token)


@blueprint.route("/logout", methods=[http.HTTPMethod.POST])
def logout():
    response = flask.jsonify({"msg": "logout successful"})
    flask_jwt_extended.unset_jwt_cookies(response)
    return response


@blueprint.after_request
def refresh_expiring_jwts(response: flask.Response):
    try:
        response.delete_cookie("access_token_cookie")
        token = utils.get_new_token_if_expired()
        if token:
            flask_jwt_extended.set_access_cookies(response, token)
        return response
    except (RuntimeError, KeyError):
        return response


@blueprint.route("/test", methods=["GET"])
@flask_jwt_extended.jwt_required()
def test():
    current_user = flask_jwt_extended.get_jwt_identity()
    claims = flask_jwt_extended.get_jwt()
    return flask.jsonify({"user": current_user, "claims": claims})
