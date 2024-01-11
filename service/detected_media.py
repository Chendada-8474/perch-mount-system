from sqlalchemy.orm import Session
from service.db_engine import db_engine
from service.query_utils import (
    get_section_indice_by_perch_mount_id,
    get_individauls_from_media,
    pop_media_individual,
)
from src.model import DetectedMedia, DetectedIndividuals


def get_empty_media(
    section_id: int = None,
    perch_mount_id: int = None,
    offset: int = 0,
    limit: int = 250,
) -> list[DetectedMedia]:
    with Session(db_engine) as session:
        query = session.query(DetectedMedia)
        if section_id:
            query = query.filter(DetectedMedia.section == section_id)
        if perch_mount_id:
            section_indice = get_section_indice_by_perch_mount_id(perch_mount_id)
            query = query.filter(DetectedMedia.section.in_(section_indice))
        query = query.offset(offset).limit(limit)
        results = query.all()
    return results


def add_media_individuals(detected_media: list[dict]):
    individauls = get_individauls_from_media(detected_media)
    detected_media = pop_media_individual(detected_media)
    new_meida: list[DetectedMedia] = []
    new_individuals: list[DetectedIndividuals] = []
    for medium in detected_media:
        new_meida.append(DetectedMedia(**medium))
    for individual in individauls:
        new_individuals.append(DetectedIndividuals(**individual))

    with Session(db_engine) as session:
        try:
            session.add_all(new_meida)
            session.flush()
            session.add_all(new_individuals)
            session.commit()
        except:
            session.rollback()
            raise


def checked_detected_media(medium_indice: list[str]):
    with Session(db_engine) as session:
        session.query(DetectedMedia).filter(
            DetectedMedia.detected_medium_id.in_(medium_indice)
        ).update({"reviewed": True})
        session.commit()


def delete_checked_detected_media():
    reviewed_medium_indice = _get_reviewed_detected_medium_indice()

    with Session(db_engine) as session:
        try:
            session.query(DetectedMedia).filter(DetectedMedia.reviewed == True).delete()
            session.query(DetectedIndividuals).filter(
                DetectedIndividuals.pending_individual_id.in_(reviewed_medium_indice)
            ).delete()
            session.commit()
        except:
            session.rollback()
            raise


def _get_reviewed_detected_medium_indice() -> list[str]:
    with Session(db_engine) as session:
        results = (
            session.query(DetectedMedia.detected_medium_id)
            .filter(DetectedMedia.reviewed == True)
            .all()
        )
    return results
