import service
from src import model


def get_behaviors() -> list[model.Behaviors]:
    with service.session.begin() as session:
        results = session.query(model.Behaviors).all()
    return results


def add_behavior(chinese_name: str) -> int:
    new_behavior = model.Behaviors(chinese_name=chinese_name)
    with service.session.begin() as session:
        session.add(new_behavior)
        session.commit()
    return new_behavior
