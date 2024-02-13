import service
from src import model
from service import query_utils


def get_detected_media(
    section_id: int = None,
    perch_mount_id: int = None,
    offset: int = 0,
    limit: int = 250,
) -> list[model.DetectedMedia]:
    with service.session.begin() as session:
        query = session.query(model.DetectedMedia)
        if section_id:
            query = query.filter(model.DetectedMedia.section == section_id)
        if perch_mount_id:
            section_indice = query_utils.get_section_indice_by_perch_mount_id(
                perch_mount_id
            )
            query = query.filter(model.DetectedMedia.section.in_(section_indice))
        query = query.offset(offset).limit(limit)
        results = query.all()
    return results


def add_media_individuals(detected_media: list[dict]):
    new_meida, new_individuals = query_utils.meida_to_insert_format(detected_media)

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


def detect(empty_indices: list[str], detected_media: list[dict]):
    new_meida, new_individuals = query_utils.meida_to_insert_format(detected_media)
    with service.session.begin() as session:
        try:
            session.query(model.EmptyMedia).filter(
                model.EmptyMedia.empty_medium_id.in_(empty_indices)
            ).delete()
            session.add_all(new_meida)
            session.flush()
            session.add_all(new_individuals)
            session.commit()
        except:
            session.rollback()
            raise
