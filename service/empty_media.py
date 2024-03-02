import service
from service import query_utils
from src import model


def get_empty_media(
    section_id: int = None,
    perch_mount_id: int = None,
    offset: int = 0,
    limit: int = 250,
    order_by_datetime: bool = True,
) -> list[model.EmptyMedia]:
    with service.session.begin() as session:
        query = session.query(model.EmptyMedia)
        if section_id:
            query = query.filter(model.EmptyMedia.section == section_id)
        if perch_mount_id:
            section_indice = query_utils.get_section_indice_by_perch_mount_id(
                perch_mount_id
            )
            query = query.filter(model.EmptyMedia.section.in_(section_indice))
        if order_by_datetime:
            query = query.order_by(model.EmptyMedia.medium_datetime)
        query = query.offset(offset).limit(limit)
        results = query.all()
    return results


def add_empty_media(empty_media: list[dict]):
    new_media = [model.EmptyMedia(**medium) for medium in empty_media]
    with service.session.begin() as session:
        session.add_all(new_media)
        session.commit()


def checked_empty_media(medium_indice: list[str]):
    with service.session.begin() as session:
        session.query(model.EmptyMedia).filter(
            model.EmptyMedia.empty_medium_id.in_(medium_indice)
        ).update()
        session.commit()


def delete_checked_empty_media():
    with service.session.begin() as session:
        session.query(model.EmptyMedia).filter(
            model.EmptyMedia.checked == True
        ).delete()
        session.commit()


def empty_check(true_empty_indice: list[str], false_empty_media: list[dict]):
    new_media = [
        model.DetectedMedia(
            detected_medium_id=medium["detected_medium_id"],
            medium_datetime=medium["medium_datetime"],
            section=medium["section"],
            empty_checker=medium["empty_checker"],
            path=medium["path"],
        )
        for medium in false_empty_media
    ]

    with service.session.begin() as session:
        try:
            session.query(model.EmptyMedia).filter(
                model.EmptyMedia.empty_medium_id.in_(true_empty_indice)
            ).update({"checked": True})
            session.add_all(new_media)
            session.commit()
        except:
            session.rollback()
