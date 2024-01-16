from sqlalchemy.orm import Session
from service import db_engine
from src.model import Positions


def get_positions() -> list[Positions]:
    with Session(db_engine) as session:
        results = session.query(Positions).all()
    return results


def add_position(name: str) -> int:
    new_position = Positions(name=name)
    with Session(db_engine) as session:
        session.add(new_position)
        session.commit()
    return new_position.position_id
