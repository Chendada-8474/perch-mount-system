from sqlalchemy.orm import Session
from service.db_engine import db_engine
from src.model import Individuals


def get_individauls_by_medium_indice(medium_indice: list[str]) -> list[Individuals]:
    with Session(db_engine) as session:
        results = (
            session.query(Individuals)
            .filter(Individuals.medium.in_(medium_indice))
            .all()
        )
    return results


def get_individauls_by_medium_indice(medium_id: str) -> list[Individuals]:
    with Session(db_engine) as session:
        result = (
            session.query(Individuals).filter(Individuals.medium == medium_id).one()
        )
    return result


def update_individaul(individual_id: int, arg: dict):
    with Session(db_engine) as session:
        session.query(Individuals).filter(
            Individuals.individual_id == individual_id
        ).update(arg)
        session.commit()
