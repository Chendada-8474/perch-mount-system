from sqlalchemy.orm import Session
from service.db_engine import db_engine
from src.model import MountTypes


def get_layers() -> list[MountTypes]:
    with Session(db_engine) as session:
        results = session.query(MountTypes).all()
    return results


def add_layer(name: str) -> int:
    new_mount_type = MountTypes(name=name)
    with Session(db_engine) as session:
        session.add(new_mount_type)
        session.commit()
    return new_mount_type.mount_type_id
