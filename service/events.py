from sqlalchemy.orm import Session
from service.db_engine import db_engine
from src.model import Events


def get_events() -> list[Events]:
    with Session(db_engine) as session:
        results = session.query(Events).all()
    return results


def add_event(chinese_name: str, english_name: str) -> int:
    new_event = Events(model_name=chinese_name, english_name=english_name)
    with Session(db_engine) as session:
        session.add(new_event)
        session.commit()
    return new_event.event_id
