from service import members

UNAUTH_MES = "Bad username or password"


def login(username: str, phone_number: str) -> bool:
    member = members.get_member_by_username(username)
    return member is not None and member.phone_number == phone_number
