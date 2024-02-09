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
            .first()
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
