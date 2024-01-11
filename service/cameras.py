from sqlalchemy.orm import Session
from service.db_engine import db_engine
from src.model import Events


def get_cameras() -> list[Events]:
    with Session(db_engine) as session:
        results = session.query(Events).all()
    return results


def add_camera(model_name: str) -> int:
    new_camera = Events(model_name=model_name)
    with Session(db_engine) as session:
        session.add(new_camera)
        session.commit()
    return new_camera.camera_id
