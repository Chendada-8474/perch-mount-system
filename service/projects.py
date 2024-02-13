import service
from src import model


def get_projects() -> list[model.Projects]:
    with service.session.begin() as session:
        results = session.query(model.Projects).all()
    return results


def get_projects_by_indice(indice: list[int]) -> list[model.Projects]:
    with service.session.begin() as session:
        results = (
            session.query(model.Projects)
            .filter(model.Projects.project_id.in_(indice))
            .all()
        )
    return results


def get_project_by_id(project_id: int) -> model.Projects:
    with service.session.begin() as session:
        result = (
            session.query(model.Projects)
            .filter(model.Projects.project_id == project_id)
            .first()
        )
    return result


def add_project(name: str) -> model.Projects:
    new_project = model.Projects(name=name)
    with service.session.begin() as session:
        session.add(new_project)
        session.commit()
    return new_project
