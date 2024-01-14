from sqlalchemy.orm import Session
from service import db_engine
from src.model import Projects


def get_layers() -> list[Projects]:
    with Session(db_engine) as session:
        results = session.query(Projects).all()
    return results


def add_layer(name: str) -> int:
    new_project = Projects(name=name)
    with Session(db_engine) as session:
        session.add(new_project)
        session.commit()
    return new_project.project_id
