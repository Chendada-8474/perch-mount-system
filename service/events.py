import service
from src import model


def get_events() -> list[model.Events]:
    with service.session.begin() as session:
        results = session.query(model.Events).all()
    return results


def add_event(chinese_name: str, english_name: str) -> model.Events:
    new_event = model.Events(model_name=chinese_name, english_name=english_name)
    with service.session.begin() as session:
        session.add(new_event)
        session.commit()
    return new_event
