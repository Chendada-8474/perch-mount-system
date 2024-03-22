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
    response = flask.jsonify({"login": True})
    response.delete_cookie("access_token_cookie")
    flask_jwt_extended.set_access_cookies(response, access_token)
    return response


@blueprint.route("/logout", methods=[http.HTTPMethod.POST])
def logout():
    response = flask.jsonify({"msg": "logout successful"})
    flask_jwt_extended.unset_jwt_cookies(response)
    return response


@blueprint.route("/me", methods=["GET"])
@flask_jwt_extended.jwt_required()
def me():
    current_user = flask_jwt_extended.get_jwt_identity()
    claims = flask_jwt_extended.get_jwt()
    print(current_user)
    return flask.jsonify(
        {
            "user": current_user,
            "user_id": claims["user_id"],
            "is_admin": claims["is_admin"],
            "is_super_admin": claims["is_super_admin"],
        }
    )
