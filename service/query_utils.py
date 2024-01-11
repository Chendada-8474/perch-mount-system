from sqlalchemy.orm import Session
from service.db_engine import db_engine
from src.model import Sections


def get_section_indice_by_perch_mount_id(perch_mount_id: int) -> list[int]:
    with Session(db_engine) as session:
        results = (
            session.query(Sections.section_id)
            .filter(Sections.perch_mount == perch_mount_id)
            .all()
        )
    return [row.section_id for row in results]


def get_individauls_from_media(media: list[dict]) -> list[dict]:
    individuals = []
    for medium in media:
        for individual in medium["individuals"]:
            individual["medium"] = medium["medium_id"]
            individuals.append(individual)
    return individuals


def pop_media_individual(media: list[dict]) -> list[dict]:
    for medium in media:
        medium.pop("individuals")
    return media
