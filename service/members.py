from sqlalchemy.orm import Session
from service import db_engine
from src.model import Members, SectionOperators


def get_members() -> list[Members]:
    with Session(db_engine) as session:
        results = session.query(Members).all()
    return results


def get_operators_by_section_indice(indice: list[int]) -> list[Members]:
    with Session(db_engine) as session:
        results = (
            session.query(Members)
            .filter(SectionOperators.section.in_(indice))
            .join(SectionOperators, SectionOperators.operator == Members.member_id)
            .all()
        )
    return results


def get_member_by_indice(indice: list[int]) -> list[Members]:
    with Session(db_engine) as session:
        result = session.query(Members).filter(Members.member_id.in_(indice)).all()
    return result


def get_member_by_id(member_id: int) -> Members:
    with Session(db_engine) as session:
        result = session.query(Members).filter(Members.member_id == member_id).first()
    return result
