import service
from src import model


def get_mount_types() -> list[model.MountTypes]:
    with service.session.begin() as session:
        results = session.query(model.MountTypes).all()
    return results


def get_mount_type_by_id(mount_type_id: int) -> model.MountTypes:
    with service.session.begin() as session:
        result = (
            session.query(model.MountTypes)
            .filter(model.MountTypes.mount_type_id == mount_type_id)
            .first()
        )
    return result


def get_mount_types_by_indice(indice: list[int]) -> list[model.MountTypes]:
    with service.session.begin() as session:
        results = (
            session.query(model.MountTypes)
            .filter(model.MountTypes.mount_type_id.in_(indice))
            .all()
        )
    return results


def add_mount_types(name: str) -> model.MountTypes:
    new_mount_type = model.MountTypes(name=name)
    with service.session.begin() as session:
        session.add(new_mount_type)
        session.commit()
    return new_mount_type
