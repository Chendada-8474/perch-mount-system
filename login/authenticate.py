import service.members
from src.model import Members

UNAUTH_MES = "Bad username or password"


def get_user_if_autherized(username: str, phone_number: str) -> Members:
    return service.members.get_member_by_authentication(username, phone_number)
