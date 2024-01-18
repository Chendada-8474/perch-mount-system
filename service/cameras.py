from sqlalchemy.orm import Session
from service import db_engine
from src.model import Cameras


def get_cameras() -> list[Cameras]:
    with Session(db_engine) as session:
        results = session.query(Cameras).all()
    return results


def add_camera(model_name: str) -> Cameras:
    new_camera = Cameras(model_name=model_name)
    with Session(db_engine) as session:
        session.add(new_camera)
        session.commit()
    return new_camera
