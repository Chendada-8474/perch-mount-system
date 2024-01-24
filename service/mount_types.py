from sqlalchemy.orm import Session
from service import db_engine
from src.model import MountTypes


def get_mount_types() -> list[MountTypes]:
    with Session(db_engine) as session:
        results = session.query(MountTypes).all()
    return results


def get_mount_type_by_id(mount_type_id: int) -> MountTypes:
    with Session(db_engine) as session:
        result = (
            session.query(MountTypes)
            .filter(MountTypes.mount_type_id == mount_type_id)
            .first()
        )
    return result


def get_mount_types_by_indice(indice: list[int]) -> list[MountTypes]:
    with Session(db_engine) as session:
        results = (
            session.query(MountTypes).filter(MountTypes.mount_type_id.in_(indice)).all()
        )
    return results


def add_mount_types(name: str) -> MountTypes:
    new_mount_type = MountTypes(name=name)
    with Session(db_engine) as session:
        session.add(new_mount_type)
        session.commit()
    return new_mount_type
