from sqlalchemy.orm import Session
from service import db_engine

import src.model as model


def get_members() -> list[model.Members]:
    with Session(db_engine) as session:
        results = session.query(model.Members).all()
    return results


def get_operators_by_section_indice(indice: list[int]) -> list[model.Members]:
    with Session(db_engine) as session:
        results = (
            session.query(model.Members)
            .filter(model.SectionOperators.section.in_(indice))
            .join(
                model.SectionOperators,
                model.SectionOperators.operator == model.Members.member_id,
            )
            .all()
        )
    return results


def get_member_by_indice(indice: list[int]) -> list[model.Members]:
    with Session(db_engine) as session:
        result = (
            session.query(model.Members)
            .filter(model.Members.member_id.in_(indice))
            .all()
        )
    return result


def get_member_by_id(member_id: int) -> model.Members:
    with Session(db_engine) as session:
        result = (
            session.query(model.Members)
            .filter(model.Members.member_id == member_id)
            .first()
        )
    return result


def update_member(member_id: int, arg: dict):
    with Session(db_engine) as session:
        session.query(model.Members).filter(
            model.Members.member_id == member_id
        ).update(arg)
        session.commit()


def add_member(
    user_name: str,
    first_name: str,
    last_name: str,
    position: int,
    phone_number: str,
    is_admin: bool,
) -> int:
    new_member = model.Members(
        user_name=user_name,
        first_name=first_name,
        last_name=last_name,
        position=position,
        phone_number=phone_number,
        is_admin=is_admin,
    )
    with Session(db_engine) as session:
        session.add(new_member)
        session.commit()
        new_id = new_member.member_id
    return new_id
