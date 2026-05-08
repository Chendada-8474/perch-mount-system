import sqlalchemy
import uuid


from app import model
from app.services import db
from app.error_handler import errors


def get_members() -> list[model.Members]:
    with db.session.begin() as session:
        query = session.query(model.Members)
        members = query.all()
    return members


def get_unactivated_members() -> list[model.Members]:
    with db.session.begin() as session:
        query = session.query(model.Members).filter(
            sqlalchemy.and_(
                model.Members.activated == False,
                model.Members.blocked == False,
            )
        )
        members = query.all()
    return members


def get_member_by_id(member_id: uuid.UUID) -> model.Members | None:
    with db.session.begin() as session:
        member = (
            session.query(model.Members)
            .filter(model.Members.id == member_id)
            .one_or_none()
        )
    return member


def get_super_admins() -> list[model.Members]:
    with db.session.begin() as session:
        super_admins = (
            session.query(model.Members)
            .filter(model.Members.is_super_admin == True)
            .all()
        )
    return super_admins


def get_member_by_gmail(gmail: str) -> model.Members | None:
    with db.session.begin() as session:
        member = (
            session.query(model.Members)
            .filter(sqlalchemy.or_(model.Members.gmail == gmail))
            .one_or_none()
        )
    return member


def get_member_by_sub_and_gmail(sub: str, email: str) -> model.Members | None:
    with db.session.begin() as session:
        member = (
            session.query(model.Members)
            .filter(
                sqlalchemy.or_(
                    model.Members.oidc_sub == sub,
                    model.Members.gmail == email,
                )
            )
            .one_or_none()
        )
    return member


def add_member_with_sso_info(id_token_info: dict) -> uuid.UUID:

    new_member = model.Members(
        oidc_sub=id_token_info["sub"],
        profile_picture_url=id_token_info["picture"],
        gmail=id_token_info["email"],
        display_name=id_token_info["name"],
        first_name=id_token_info["family_name"],
        last_name=id_token_info["given_name"],
    )
    with db.session.begin() as session:
        session.add(new_member)
        session.commit()
        new_id = new_member.id

    return new_id


def update_member_by_id(member_id: uuid.UUID, args: dict):
    with db.session.begin() as session:
        session.query(model.Members).filter(model.Members.id == member_id).update(args)
        session.commit()


def update_member_sso_info(id_token_info: dict):
    with db.session.begin() as session:
        session.query(model.Members).filter(
            sqlalchemy.or_(
                model.Members.oidc_sub == id_token_info["sub"],
                model.Members.gmail == id_token_info["email"],
            )
        ).update(
            {
                "oidc_sub": id_token_info["sub"],
                "display_name": id_token_info["name"],
                "first_name": id_token_info["given_name"],
                "last_name": id_token_info["family_name"],
                "profile_picture_url": id_token_info["picture"],
            }
        )
        session.commit()


def block_member(member_id: uuid.UUID):
    is_super_admin = _is_member_super_admin(member_id)

    if is_super_admin is None:
        raise errors.ResourceNotFoundError()
    if is_super_admin:
        raise errors.SuperAdminUnpatchableError()

    update_member_by_id(member_id, {"blocked": True})


def unblock_member(member_id: uuid.UUID):
    update_member_by_id(member_id, {"blocked": False})


def activate_member(member_id: uuid.UUID):
    is_super_admin = _is_member_super_admin(member_id)

    if is_super_admin is None:
        raise errors.ResourceNotFoundError()
    if is_super_admin:
        raise errors.SuperAdminUnpatchableError()

    update_member_by_id(member_id, {"activated": True})


def deactivate_member(member_id: uuid.UUID):
    is_super_admin = _is_member_super_admin(member_id)

    if is_super_admin is None:
        raise errors.ResourceNotFoundError()
    if is_super_admin:
        raise errors.SuperAdminUnpatchableError()

    update_member_by_id(member_id, {"activated": False})


def grant_admin_privileges(member_id: uuid.UUID):
    is_super_admin = _is_member_super_admin(member_id)

    if is_super_admin is None:
        raise errors.ResourceNotFoundError()
    if is_super_admin:
        raise errors.SuperAdminUnpatchableError()

    update_member_by_id(member_id, {"is_admin": True})


def ungrant_admin_privileges(member_id: uuid.UUID):
    is_super_admin = _is_member_super_admin(member_id)

    if is_super_admin is None:
        raise errors.ResourceNotFoundError()
    if is_super_admin:
        raise errors.SuperAdminUnpatchableError()

    update_member_by_id(member_id, {"is_admin": False})


def grant_super_admin_privileges(member_id: uuid.UUID):
    update_member_by_id(member_id, {"is_admin": True, "is_super_admin": True})


def ungrant_super_admin_privileges(member_id: uuid.UUID):
    update_member_by_id(member_id, {"is_super_admin": False})


def _is_member_super_admin(member_id: uuid.UUID) -> bool | None:
    with db.session.begin() as session:
        member: model.Members = (
            session.query(model.Members.is_super_admin)
            .filter(model.Members.id == member_id)
            .one_or_none()
        )

    if member is None:
        return

    return member.is_super_admin


def init_first_member(gmail: str, first_name: str, last_name: str):
    member = get_member_by_gmail(gmail)
    super_admins = get_super_admins()

    if super_admins or member:
        return

    first_member = model.Members(
        gmail=gmail,
        first_name=first_name,
        last_name=last_name,
        is_admin=True,
        is_super_admin=True,
        activated=True,
    )
    with db.session.begin() as session:
        session.add(first_member)
        session.commit()
