from sqlalchemy.orm import Session
from service.db_engine import db_engine
from service.query_utils import get_section_indice_by_perch_mount_id
from src.model import EmptyMedia


def get_empty_media(
    section_id: int = None,
    perch_mount_id: int = None,
    offset: int = 0,
    limit: int = 250,
) -> list[EmptyMedia]:
    with Session(db_engine) as session:
        query = session.query(EmptyMedia)
        if section_id:
            query = query.filter(EmptyMedia.section == section_id)
        if perch_mount_id:
            section_indice = get_section_indice_by_perch_mount_id(perch_mount_id)
            query = query.filter(EmptyMedia.section.in_(section_indice))
        query = query.offset(offset).limit(limit)
        results = query.all()
    return results


def add_empty_media(empty_media: list[dict]):
    new_media = [EmptyMedia(**medium) for medium in empty_media]
    with Session(db_engine) as session:
        session.add_all(new_media)
        session.commit()


def checked_empty_media(medium_indice: list[str]):
    with Session(db_engine) as session:
        session.query(EmptyMedia).filter(
            EmptyMedia.empty_medium_id.in_(medium_indice)
        ).update()
        session.commit()


def delete_checked_empty_media():
    with Session(db_engine) as session:
        session.query(EmptyMedia).filter(EmptyMedia.checked == True).delete()
        session.commit()
