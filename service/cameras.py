import service
from src import model


def get_cameras() -> list[model.Cameras]:
    with service.session.begin() as session:
        results = session.query(model.Cameras).all()
    return results


def get_camera_by_id(camera_id: int) -> model.Cameras:
    with service.session.begin() as session:
        result = (
            session.query(model.Cameras)
            .filter(model.Cameras.camera_id == camera_id)
            .first()
        )
    return result


def add_camera(model_name: str) -> int:
    new_camera = model.Cameras(model_name=model_name)
    with service.session.begin() as session:
        session.add(new_camera)
        session.commit()
    return new_camera.camera_id
