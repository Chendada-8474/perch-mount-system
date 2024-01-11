from sqlalchemy.orm import Session
from service.db_engine import db_engine
from src.model import Members


def get_members() -> list[Members]:
    with Session(db_engine) as session:
        results = session.query(Members).all()
    return results


def get_member_by_id(member_id: int) -> Members:
    with Session(db_engine) as session:
        result = session.query(Members).filter(Members.member_id == member_id).one()
    return result
