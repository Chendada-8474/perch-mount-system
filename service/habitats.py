from sqlalchemy.orm import Session
from service import db_engine
from src.model import Habitats


def get_habitats() -> list[Habitats]:
    with Session(db_engine) as session:
        results = session.query(Habitats).all()
    return results


def add_habitat(chinese_name: str, english_name: str) -> int:
    new_habitat = Habitats(
        chinese_name=chinese_name,
        english_name=english_name,
    )
    with Session(db_engine) as session:
        session.add(new_habitat)
        session.commit()
    return new_habitat.habitat_id
