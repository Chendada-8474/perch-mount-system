import sqlalchemy.orm
from service import db_engine
from service import query_utils
from src.model import EmptyMedia


def get_empty_media(
    section: int = None,
    perch_mount: int = None,
    offset: int = 0,
    limit: int = 250,
    order_by_datetime: bool = True,
) -> list[EmptyMedia]:
    with sqlalchemy.orm.Session(db_engine) as session:
        query = session.query(EmptyMedia)
        if section:
            query = query.filter(EmptyMedia.section == section)
        if perch_mount:
            section_indice = query_utils.get_section_indice_by_perch_mount_id(
                perch_mount
            )
            query = query.filter(EmptyMedia.section.in_(section_indice))
        if order_by_datetime:
            query = query.order_by(EmptyMedia.medium_datetime)
        query = query.offset(offset).limit(limit)
        results = query.all()
    return results


def add_empty_media(empty_media: list[dict]):
    new_media = [EmptyMedia(**medium) for medium in empty_media]
    with sqlalchemy.orm.Session(db_engine) as session:
        session.add_all(new_media)
        session.commit()


def checked_empty_media(medium_indice: list[str]):
    with sqlalchemy.orm.Session(db_engine) as session:
        session.query(EmptyMedia).filter(
            EmptyMedia.empty_medium_id.in_(medium_indice)
        ).update()
        session.commit()


def delete_checked_empty_media():
    with sqlalchemy.orm.Session(db_engine) as session:
        session.query(EmptyMedia).filter(EmptyMedia.checked == True).delete()
        session.commit()
