from sqlalchemy.orm import Session
from service.db_engine import db_engine
from src.model import Species, Individuals


def get_species(
    recorded: bool = None,
    category: str = None,
    order: str = None,
    family: str = None,
    conservation: str = None,
) -> list[Species]:
    with Session(db_engine) as session:
        query = session.query(Species)

        if recorded:
            taxon_orders = _get_recorded_taxon_order()
            query = query.filter(Species.taxon_order.in_(taxon_orders))
        if category:
            query = query.filter(Species.category == category)
        if order:
            query = query.filter(Species.order == order)
        if family:
            query = query.filter(Species.family_latin_name == family)
        if conservation:
            query = query.filter(Species.conservation_status == conservation.upper())

        results = query.all()

    return results


def _get_recorded_taxon_order() -> list[int]:
    with Session(db_engine) as session:
        results = session.query(Individuals.taxon_order_by_human).distinct().all()
    return [row.taxon_order_by_human for row in results]
