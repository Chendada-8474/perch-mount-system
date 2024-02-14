import flask
import flask_jwt_extended
import http

from src import app
from login import authenticate
from login import utils


@app.app.route("/login", methods=[http.HTTPMethod.POST])
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


@app.app.route("/logout", methods=[http.HTTPMethod.POST])
def logout():
    response = flask.jsonify({"msg": "logout successful"})
    flask_jwt_extended.unset_jwt_cookies(response)
    return response


@app.app.after_request
def refresh_expiring_jwts(response: flask.Response):
    try:
        response.delete_cookie("access_token_cookie")
        token = utils.get_new_token_if_expired()
        if token:
            flask_jwt_extended.set_access_cookies(response, token)
        return response
    except (RuntimeError, KeyError):
        return response
