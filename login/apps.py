from datetime import timedelta
import flask
import flask_jwt_extended
import http


from login import jwt_redis_blocklist, jwt
from login import authenticate
from login import utils

blueprint = flask.Blueprint("login", __name__)

ACCESS_EXPIRES = timedelta(hours=1)


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
    return flask.jsonify({"token": access_token})


@blueprint.route("/logout", methods=[http.HTTPMethod.DELETE])
@flask_jwt_extended.jwt_required()
def logout():
    jti = flask_jwt_extended.get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return flask.jsonify(msg="Access token revoked")


@blueprint.route("/me", methods=["GET"])
@flask_jwt_extended.jwt_required()
def me():
    current_user = flask_jwt_extended.get_jwt_identity()
    claims = flask_jwt_extended.get_jwt()
    return flask.jsonify(
        {
            "user": current_user,
            "user_id": claims["user_id"],
            "is_admin": claims["is_admin"],
            "is_super_admin": claims["is_super_admin"],
        }
    )


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
