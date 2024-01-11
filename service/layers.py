from sqlalchemy.orm import Session
from service.db_engine import db_engine
from src.model import Layers


def get_layers() -> list[Layers]:
    with Session(db_engine) as session:
        results = session.query(Layers).all()
    return results


def add_layer(name: str) -> int:
    new_layer = Layers(name=name)
    with Session(db_engine) as session:
        session.add(new_layer)
        session.commit()
    return new_layer.layer_id