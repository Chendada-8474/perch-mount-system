from datetime import datetime, timezone, timedelta
import flask_jwt_extended

import login.utils
import service.members
from src import config
from src.model import Members


def get_new_token_if_expired() -> str | None:
    token = None
    expired_timestamp = flask_jwt_extended.get_jwt()["exp"]
    now = datetime.now(timezone(timedelta(hours=8)))
    target_timestamp = datetime.timestamp(now + config.get_jwt_refresh_expires())
    if target_timestamp > expired_timestamp:

        identity = flask_jwt_extended.get_jwt_identity()
        member = service.members.get_member_by_username(identity)
        claims = login.utils.get_authorization_claims(member)

        token = flask_jwt_extended.create_access_token(
            identity=identity, additional_claims=claims
        )
    return token


def get_authorization_claims(login_user: Members) -> dict:
    return {
        "user_id": login_user.member_id,
        "is_admin": login_user.is_admin,
        "is_super_admin": login_user.is_super_admin,
    }
