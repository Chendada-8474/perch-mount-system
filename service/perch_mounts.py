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
            .filter(model.EmptyMedia.section != None)
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
            .filter(model.DetectedMedia.section != None)
            .group_by(model.DetectedMedia.section)
        ).all()

        media = (
            session.query(
                model.Media.section,
                sqlalchemy.func.count(model.Media.medium_id).label("count"),
            )
            .filter(model.Media.section.in_(section_indice))
            .filter(model.Media.section != None)
            .group_by(model.Media.section)
        ).all()

        prey = (
            session.query(
                model.Media.section,
                sqlalchemy.func.count(model.Individuals.individual_id).label("count"),
            )
            .join(model.Individuals, model.Individuals.medium == model.Media.medium_id)
            .filter(model.Individuals.prey == True and not model.Individuals.prey_name)
            .filter(model.Media.section != None)
            .group_by(model.Media.section)
            .all()
        )

    return {
        "empty": {row.section: row.count for row in empty},
        "detected": {row.section: row.count for row in detected},
        "media": {row.section: row.count for row in media},
        "prey": {row.section: row.count for row in prey},
    }


def perch_mounts_pending_media_count():
    with service.session.begin() as session:
        empty = (
            session.query(
                model.Sections.perch_mount,
                sqlalchemy.func.count(model.EmptyMedia.empty_medium_id).label(
                    "empty_count"
                ),
            )
            .filter(model.EmptyMedia.checked == False)
            .join(model.Sections, model.Sections.section_id == model.EmptyMedia.section)
            .group_by(model.Sections.perch_mount)
            .subquery()
        )
        detected = (
            session.query(
                model.Sections.perch_mount,
                sqlalchemy.func.count(model.DetectedMedia.detected_medium_id).label(
                    "detected_count"
                ),
            )
            .filter(model.DetectedMedia.reviewed == False)
            .join(
                model.Sections, model.Sections.section_id == model.DetectedMedia.section
            )
            .group_by(model.Sections.perch_mount)
            .subquery()
        )

        results = (
            session.query(
                model.PerchMounts.perch_mount_id,
                model.PerchMounts.perch_mount_name,
                model.PerchMounts.project,
                model.PerchMounts.claim_by,
                detected.c.detected_count,
                empty.c.empty_count,
            )
            .join(
                empty,
                empty.c.perch_mount == model.PerchMounts.perch_mount_id,
                isouter=True,
            )
            .join(
                detected,
                detected.c.perch_mount == model.PerchMounts.perch_mount_id,
                isouter=True,
            )
            .order_by(model.PerchMounts.perch_mount_id)
            .filter(
                sqlalchemy.or_(detected.c.detected_count > 0, empty.c.empty_count > 0)
            )
            .all()
        )

    return results
