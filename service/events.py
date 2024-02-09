import service
from src import model


def get_events() -> list[model.Events]:
    with service.session.begin() as session:
        results = session.query(model.Events).all()
    return results


def get_event_by_id(event_id: int) -> model.Events:
    with service.session.begin() as session:
        result = (
            session.query(model.Events).filter(model.Events.event_id == event_id).one()
        )
    return result


def add_event(chinese_name: str, english_name: str) -> int:
    new_event = model.Events(model_name=chinese_name, english_name=english_name)
    with service.session.begin() as session:
        session.add(new_event)
        session.commit()
    return new_event.event_id
