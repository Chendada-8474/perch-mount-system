from sqlalchemy.orm import Session
from service import db_engine
from src.model import Habitats


def get_habitats() -> list[Habitats]:
    with Session(db_engine) as session:
        results = session.query(Habitats).all()
    return results


def get_habitats_by_indice(indice: list[int]) -> list[Habitats]:
    with Session(db_engine) as session:
        results = session.query(Habitats).filter(Habitats.habitat_id.in_(indice)).all()
    return results


def get_habitat_by_id(habitat_id: int) -> Habitats:
    with Session(db_engine) as session:
        result = (
            session.query(Habitats).filter(Habitats.habitat_id == habitat_id).first()
        )
    return result


def add_habitat(chinese_name: str, english_name: str) -> Habitats:
    new_habitat = Habitats(
        chinese_name=chinese_name,
        english_name=english_name,
    )
    with Session(db_engine) as session:
        session.add(new_habitat)
        session.commit()
    return new_habitat
