from sqlalchemy.orm import Session
from service.db_engine import db_engine
from src.model import Species, Individuals


def get_species() -> list[Species]:
    with Session(db_engine) as session:
        results = session.query(Species).all()
    return results


def get_species_by_taxon_orders(taxon_orders: list[int]) -> list[Species]:
    with Session(db_engine) as session:
        results = (
            session.query(Species).filter(Species.taxon_order.in_(taxon_orders)).all()
        )
    return results
