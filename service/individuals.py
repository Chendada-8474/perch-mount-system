import service
from src import model


def get_individauls_by_medium_indice(
    medium_indice: list[str],
) -> list[model.Individuals]:
    with service.session.begin() as session:
        results = (
            session.query(model.Individuals)
            .filter(model.Individuals.medium.in_(medium_indice))
            .all()
        )
    return results


def get_individauls_by_medium_id(medium_id: str) -> list[model.Individuals]:
    with service.session.begin() as session:
        result = (
            session.query(model.Individuals)
            .filter(model.Individuals.medium == medium_id)
            .one()
        )
    return result


def update_individaul(individual_id: int, arg: dict):
    with service.session.begin() as session:
        session.query(model.Individuals).filter(
            model.Individuals.individual_id == individual_id
        ).update(arg)
        session.commit()
