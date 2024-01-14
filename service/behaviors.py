from sqlalchemy.orm import Session
from service import db_engine
from src.model import Positions


def get_behaviors() -> list[Positions]:
    with Session(db_engine) as session:
        results = session.query(Positions).all()
    return results


def add_behavior(chinese_name: str) -> int:
    new_behavior = Positions(chinese_name=chinese_name)
    with Session(db_engine) as session:
        session.add(new_behavior)
        session.commit()
    return new_behavior.behavior_id
