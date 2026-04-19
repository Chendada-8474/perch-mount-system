import uuid

from app.services import db
import app.services.perchai.utils as services_utils
from app import model
from app.error_handler import errors
from app.model import enums


def get_individual_by_id(individual_id: uuid.UUID) -> model.Individuals | None:
    with db.session.begin() as session:
        individual = (
            session.query(model.Individuals)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )
    return individual


def update_individual(individual_id: uuid.UUID, args: dict):
    with db.session.begin() as session:
        individual = (
            session.query(model.Individuals.medium_id)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        medium = (
            session.query(model.Media.status)
            .filter(model.Media.id == individual.medium_id)
            .one()
        )

        if medium.status != model.enums.MediaStatus.REVIEWED:
            raise errors.StatusError(medium.status)

        try:
            session.query(model.ReviewedIndividualsContents).filter(
                model.ReviewedIndividualsContents.individual_id == individual_id
            ).update(args)

            session.commit()
        except:
            session.rollback()
            raise


def get_prey_by_individual_id(
    individual_id: uuid.UUID,
) -> model.IdentifiedPreyIndividualsContents | None:
    with db.session.begin() as session:
        prey = (
            session.query(model.IdentifiedPreyIndividualsContents.individual_id)
            .filter(
                model.IdentifiedPreyIndividualsContents.individual_id == individual_id
            )
            .one_or_none()
        )
    return prey


def add_prey(
    individual_id: uuid.UUID,
    args: dict,
):
    with db.session.begin() as session:
        individual = (
            session.query(model.Individuals.prey_status)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        if individual.prey_status != model.enums.PreyStatus.NO_PREY:
            raise errors.StatusError(individual.prey_status)

        new_prey = model.IdentifiedPreyIndividualsContents(**args)
        new_prey.individual_id = individual_id

        try:
            session.query(model.MarkedPreyIndividualsContents).filter(
                model.MarkedPreyIndividualsContents.individual_id == individual_id
            ).update({"has_prey": True})
            session.add(new_prey)
            session.commit()
        except:
            session.rollback()
            raise


def update_prey(
    individual_id: uuid.UUID,
    args: dict,
):
    with db.session.begin() as session:
        individual = (
            session.query(model.Individuals.prey_status)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        if individual.prey_status != model.enums.PreyStatus.IDENTIFIED:
            raise errors.StatusError(individual.prey_status)

        try:
            session.query(model.IdentifiedPreyIndividualsContents).filter(
                model.IdentifiedPreyIndividualsContents.individual_id == individual_id
            ).update(args)
            session.commit()
        except:
            session.rollback()
            raise


def delete_prey(individual_id: uuid.UUID):
    with db.session.begin() as session:
        individual = (
            session.query(model.Individuals.prey_status)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        if individual.prey_status != model.enums.PreyStatus.IDENTIFIED:
            raise errors.StatusError(individual.prey_status)

        try:
            session.query(model.MarkedPreyIndividualsContents).filter(
                model.MarkedPreyIndividualsContents.individual_id == individual_id
            ).update({"has_prey": False})
            session.query(model.IdentifiedPreyIndividualsContents).filter(
                model.IdentifiedPreyIndividualsContents.individual_id == individual_id
            ).delete(synchronize_session=False)
            session.commit()
        except:
            session.rollback()
            raise


def upsert_note(individual_id: uuid.UUID, note: str):
    with db.session.begin() as session:
        individual = (
            session.query(model.Individuals)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        try:
            session.query(model.Individuals).filter(
                model.Individuals.id == individual_id
            ).update({"note": note})
            session.commit()
        except:
            session.rollback()
            raise


def remove_note(individual_id: uuid.UUID):
    with db.session.begin() as session:
        individual = (
            session.query(model.Individuals)
            .filter(model.Individuals.id == individual_id)
            .one_or_none()
        )

        if not individual:
            raise errors.ResourceNotFoundError(model.Individuals.__name__)

        try:
            session.query(model.Individuals).filter(
                model.Individuals.id == individual_id
            ).update({"note": None})
            session.commit()
        except:
            session.rollback()
            raise


def add_identified_preys(identified_preys: list[dict]):
    preys = []
    no_prey_individual_ids = []

    for prey in identified_preys:
        if prey["inaturalist_taxa_id"]:
            preys.append(model.IdentifiedPreyIndividualsContents(**prey))
        else:
            no_prey_individual_ids.append(prey["individual_id"])

    with db.session.begin() as session:
        try:
            session.add_all(preys)
            session.query(model.Individuals).filter(
                model.Individuals.id.in_(no_prey_individual_ids)
            ).update({"prey_status": enums.PreyStatus.NO_PREY})
            session.commit()
        except:
            session.rollback()
            raise


def get_individuals_by_filter(
    filter: services_utils.IndividualsFilter,
) -> list[model.Individuals]:
    modifier = services_utils.IndividualsQueryModifier(filter)
    with db.session.begin() as session:
        query = session.query(model.Individuals)
        query = modifier.filter_query(query)
        query = modifier.limit_query(query)
        query = modifier.offset_query(query)
        individuals = query.all()
    return individuals


def get_all_distinct_prey_inat_ids():
    with db.session.begin() as session:
        query = session.query(
            model.IdentifiedPreyIndividualsContents.inaturalist_taxa_id
        ).distinct()
    return query.all()
