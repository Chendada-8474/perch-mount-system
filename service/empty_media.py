import service
import service.query_utils
import src.model as model


def get_empty_media(
    section: int = None,
    perch_mount: int = None,
    offset: int = 0,
    limit: int = 250,
    order_by_datetime: bool = True,
) -> list[model.EmptyMedia]:
    with service.session.begin() as session:
        query = session.query(model.EmptyMedia)
        if section:
            query = query.filter(model.EmptyMedia.section == section)
        if perch_mount:
            section_indice = service.query_utils.get_section_indice_by_perch_mount_id(
                perch_mount
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
