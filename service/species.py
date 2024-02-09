import service
from src import model


def get_species(
    species: str = None,
    order: str = None,
    family: str = None,
    conservation: str = None,
) -> list[model.Species]:
    with service.session.begin() as session:
        query = session.query(model.Species)

        if species:
            query = query.filter(model.Species.category == species)
        if order:
            query = query.filter(model.Species.order == order)
        if family:
            query = query.filter(model.Species.family_latin_name == family)
        if conservation:
            query = query.filter(model.Species.conservation_status == conservation)

        results = query.all()

    return results


def get_species_by_taxon_orders(taxon_orders: list[int]) -> list[model.Species]:
    with service.session.begin() as session:
        results = (
            session.query(model.Species)
            .filter(model.Species.taxon_order.in_(taxon_orders))
            .all()
        )
    return results


def get_species_by_taxon_order(taxon_order: int) -> model.Species:
    with service.session.begin() as session:
        result = (
            session.query(model.Species)
            .filter(model.Species.taxon_order == taxon_order)
            .one()
        )
    return result
