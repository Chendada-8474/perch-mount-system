import service
from src import model


def get_positions() -> list[model.Positions]:
    with service.session.begin() as session:
        results = session.query(model.Positions).all()
    return results


def get_position_by_id(position_id: int) -> model.Positions:
    with service.session.begin() as session:
        result = (
            session.query(model.Positions)
            .filter(model.Positions.position_id == position_id)
            .one()
        )
    return result


def add_position(name: str) -> int:
    new_position = model.Positions(name=name)
    with service.session.begin() as session:
        session.add(new_position)
        session.commit()
    return new_position.position_id
