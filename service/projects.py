from sqlalchemy.orm import Session
from service import db_engine
from src.model import Projects


def get_projects() -> list[Projects]:
    with Session(db_engine) as session:
        results = session.query(Projects).all()
    return results


def get_projects_by_indice(indice: list[int]) -> list[Projects]:
    with Session(db_engine) as session:
        results = session.query(Projects).filter(Projects.project_id.in_(indice)).all()
    return results


def get_project_by_id(project_id: int) -> Projects:
    with Session(db_engine) as session:
        result = (
            session.query(Projects).filter(Projects.project_id == project_id).first()
        )
    return result


def add_project(name: str) -> Projects:
    new_project = Projects(name=name)
    with Session(db_engine) as session:
        session.add(new_project)
        session.commit()
    return new_project
