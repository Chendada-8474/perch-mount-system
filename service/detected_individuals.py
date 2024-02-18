import service
from src import model


def get_detected_individauls_by_medium_indice(
    medium_indice: list[str],
) -> list[model.DetectedIndividuals]:
    with service.session.begin() as session:
        results = (
            session.query(model.DetectedIndividuals)
            .filter(model.DetectedIndividuals.medium.in_(medium_indice))
            .all()
        )
    return results


def get_individauls_by_medium_id(medium_id: str) -> list[model.DetectedIndividuals]:
    with service.session.begin() as session:
        result = (
            session.query(model.DetectedIndividuals)
            .filter(model.DetectedIndividuals.medium == medium_id)
            .one()
        )
    return result


def update_individaul(individual_id: int, arg: dict):
    with service.session.begin() as session:
        session.query(model.DetectedIndividuals).filter(
            model.DetectedIndividuals.pending_individual_id == individual_id
        ).update(arg)
        session.commit()
