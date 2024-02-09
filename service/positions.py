import service
from src import model


def get_positions() -> list[model.Positions]:
    with service.session.begin() as session:
        results = session.query(model.Positions).all()
    return results


def add_position(name: str) -> model.Positions:
    new_position = model.Positions(name=name)
    with service.session.begin() as session:
        session.add(new_position)
        session.commit()
    return new_position
