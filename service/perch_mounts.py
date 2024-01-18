from sqlalchemy.orm import Session
from service import db_engine
from src.model import PerchMounts


def get_perch_mounts(
    project: int = None,
    habitat: int = None,
    terminated: bool = None,
    claim_by: int = None,
) -> list[PerchMounts]:
    with Session(db_engine) as session:
        query = session.query(PerchMounts)

        if project:
            query = query.filter(PerchMounts.project == project)

        if habitat:
            query = query.filter(PerchMounts.habitat == habitat)

        if terminated is not None:
            query = query.filter(PerchMounts.terminated == terminated)

        if claim_by:
            query = query.filter(PerchMounts.claim_by == claim_by)

        results = query.all()
    return results


def get_perch_mount_by_id(perch_mount_id: int):
    with Session(db_engine) as session:
        result = (
            session.query(PerchMounts)
            .filter(PerchMounts.perch_mount_id == perch_mount_id)
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
) -> PerchMounts:
    new_perch_mount = PerchMounts(
        perch_mount_name=perch_mount_name,
        latitude=latitude,
        longitude=longitude,
        habitat=habitat,
        project=project,
        layer=layer,
    )
    with Session(db_engine) as session:
        session.add(new_perch_mount)
        session.commit()
    return new_perch_mount


def update_perch_mount(perch_mount_id: int, arg: dict):
    with Session(db_engine) as session:
        session.query(PerchMounts).filter(
            PerchMounts.perch_mount_id == perch_mount_id
        ).update(arg)
        session.commit()
