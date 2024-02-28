import sqlalchemy

import service
from src import model


def get_perch_mounts(
    project: int = None,
    habitat: int = None,
    terminated: bool = None,
    claim_by: int = None,
) -> list[model.PerchMounts]:
    with service.session.begin() as session:
        query = session.query(model.PerchMounts)

        if project:
            query = query.filter(model.PerchMounts.project == project)

        if habitat:
            query = query.filter(model.PerchMounts.habitat == habitat)

        if terminated is not None:
            query = query.filter(model.PerchMounts.terminated == terminated)

        if claim_by:
            query = query.filter(model.PerchMounts.claim_by == claim_by)

        results = query.all()
    return results


def get_perch_mount_by_id(perch_mount_id: int):
    with service.session.begin() as session:
        result = (
            session.query(model.PerchMounts)
            .filter(model.PerchMounts.perch_mount_id == perch_mount_id)
            .one_or_none()
        )
    return result


def add_perch_mount(
    perch_mount_name: str,
    latitude: float,
    longitude: float,
    habitat: int,
    project: int,
    layer: int,
) -> int:
    new_perch_mount = model.PerchMounts(
        perch_mount_name=perch_mount_name,
        latitude=latitude,
        longitude=longitude,
        habitat=habitat,
        project=project,
        layer=layer,
    )
    with service.session.begin() as session:
        session.add(new_perch_mount)
        session.commit()
        new_id = new_perch_mount.perch_mount_id
    return new_id


def update_perch_mount(perch_mount_id: int, arg: dict):
    with service.session.begin() as session:
        session.query(model.PerchMounts).filter(
            model.PerchMounts.perch_mount_id == perch_mount_id
        ).update(arg)
        session.commit()


def section_media_count(perch_mount_id: int) -> dict:
    with service.session.begin() as session:
        query = (
            session.query(model.Sections.section_id)
            .join(
                model.PerchMounts,
                model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
            )
            .filter(model.PerchMounts.perch_mount_id == perch_mount_id)
        )
        section_indice = [section.section_id for section in query.all()]

        empty = (
            session.query(
                model.EmptyMedia.section,
                sqlalchemy.func.count(model.EmptyMedia.empty_medium_id).label("count"),
            )
            .filter(model.EmptyMedia.section.in_(section_indice))
            .filter(model.EmptyMedia.checked == False)
            .group_by(model.EmptyMedia.section)
        ).all()

        detected = (
            session.query(
                model.DetectedMedia.section,
                sqlalchemy.func.count(model.DetectedMedia.detected_medium_id).label(
                    "count"
                ),
            )
            .filter(model.DetectedMedia.section.in_(section_indice))
            .filter(model.DetectedMedia.reviewed == False)
            .group_by(model.DetectedMedia.section)
        ).all()

        media = (
            session.query(
                model.Media.section,
                sqlalchemy.func.count(model.Media.medium_id).label("count"),
            )
            .filter(model.Media.section.in_(section_indice))
            .group_by(model.Media.section)
        ).all()

        prey = (
            session.query(
                model.Media.section,
                sqlalchemy.func.count(model.Individuals.individual_id).label("count"),
            )
            .join(model.Individuals, model.Individuals.medium == model.Media.medium_id)
            .filter(model.Individuals.prey == True and not model.Individuals.prey_name)
            .group_by(model.Media.section)
            .all()
        )

    return {
        "empty": {row.section: row.count for row in empty},
        "detected": {row.section: row.count for row in detected},
        "media": {row.section: row.count for row in media},
        "prey": {row.section: row.count for row in prey},
    }


def _get_section_indice_by_perch_mount_id(perch_mount_id: int) -> list[int]:
    with service.session.begin() as session:
        query = (
            session.query(model.Sections.section_id)
            .join(
                model.PerchMounts,
                model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
            )
            .filter(model.PerchMounts.perch_mount_id == perch_mount_id)
        )
        section_indice = [section.section_id for section in query.all()]
    return section_indice
