import service
import sqlalchemy
from src import model
from service import query_utils


def get_detected_media(
    section_id: int = None,
    perch_mount_id: int = None,
    offset: int = 0,
    limit: int = 100,
) -> list[model.DetectedMedia]:
    with service.session.begin() as session:
        query = session.query(
            model.DetectedMedia.detected_medium_id,
            model.DetectedMedia.empty_checker,
            model.DetectedMedia.medium_datetime,
            model.DetectedMedia.path,
            model.DetectedMedia.section,
            model.Sections.check_date,
            model.PerchMounts.perch_mount_name,
            model.Projects.name.label("project_name"),
        )

        query = query.filter(model.DetectedMedia.reviewed == False)

        if section_id:
            query = query.filter(model.DetectedMedia.section == section_id)

        if perch_mount_id:
            query = query.filter(model.Sections.perch_mount == perch_mount_id)

        query = query.join(
            model.Sections,
            model.Sections.section_id == model.DetectedMedia.section,
        )
        query = query.join(
            model.PerchMounts,
            model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
        )
        query = query.join(
            model.Projects,
            model.Projects.project_id == model.PerchMounts.project,
        )
        query = query.order_by(model.DetectedMedia.medium_datetime)
        query = query.offset(offset).limit(limit)
        results = query.all()
    return results


def get_detected_medium_by_id(detected_medium_id: str):
    with service.session.begin() as session:
        query = session.query(
            model.DetectedMedia.detected_medium_id,
            model.DetectedMedia.empty_checker,
            model.DetectedMedia.medium_datetime,
            model.DetectedMedia.path,
            model.DetectedMedia.section,
            model.Sections.check_date,
            model.PerchMounts.perch_mount_name,
            model.Projects.name.label("project_name"),
        ).filter(model.DetectedMedia.detected_medium_id == detected_medium_id)
        query = query.join(
            model.Sections,
            model.Sections.section_id == model.DetectedMedia.section,
        )
        query = query.join(
            model.PerchMounts,
            model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
        )
        query = query.join(
            model.Projects,
            model.Projects.project_id == model.PerchMounts.project,
        )
        result = query.one_or_none()
    return result


def add_media_individuals(detected_media: list[dict]):
    new_meida, new_individuals = query_utils.detected_meida_to_insert_format(
        detected_media
    )

    with service.session.begin() as session:
        try:
            session.add_all(new_meida)
            session.flush()
            session.add_all(new_individuals)
            session.commit()
        except:
            session.rollback()
            raise


def checked_detected_media(medium_indice: list[str]):
    with service.session.begin() as session:
        session.query(model.DetectedMedia).filter(
            model.DetectedMedia.detected_medium_id.in_(medium_indice)
        ).update({"reviewed": True})
        session.commit()


def delete_checked_detected_media():
    reviewed_medium_indice = _get_reviewed_detected_medium_indice()

    with service.session.begin() as session:
        try:
            session.query(model.DetectedMedia).filter(
                model.DetectedMedia.reviewed == True
            ).delete()
            session.query(model.DetectedIndividuals).filter(
                model.DetectedIndividuals.pending_individual_id.in_(
                    reviewed_medium_indice
                )
            ).delete()
            session.commit()
        except:
            session.rollback()
            raise


def _get_reviewed_detected_medium_indice() -> list[str]:
    with service.session.begin() as session:
        results = (
            session.query(model.DetectedMedia.detected_medium_id)
            .filter(model.DetectedMedia.reviewed == True)
            .all()
        )
    return results


def detect(section: dict, empty_media: list[dict], detected_media: list[dict]):
    operators = [operator for operator in section["operators"]]
    section.pop("operators")
    new_section = model.Sections(**section)
    with service.session.begin() as session:
        try:
            session.add(new_section)
            session.flush()
            new_section_operators = query_utils.find_section_operators(
                new_section.section_id, operators
            )
            session.add_all(new_section_operators)
            session.query(model.PerchMounts).filter(
                model.PerchMounts.perch_mount_id == section["perch_mount"]
            ).update({"latest_note": section["note"]})

            new_detected_meida, new_detected_individuals = (
                query_utils.detected_meida_to_insert_format(
                    detected_media, new_section.section_id
                )
            )
            new_empty_media = query_utils.empty_media_to_insert_format(
                empty_media, new_section.section_id
            )
            session.add_all(new_empty_media)
            session.add_all(new_detected_meida)
            session.flush()
            session.add_all(new_detected_individuals)
            session.commit()
        except:
            session.rollback()
            raise
