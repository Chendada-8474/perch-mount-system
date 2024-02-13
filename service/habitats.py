import service
from src import model


def get_habitats() -> list[model.Habitats]:
    with service.session.begin() as session:
        results = session.query(model.Habitats).all()
    return results


def get_habitats_by_indice(indice: list[int]) -> list[model.Habitats]:
    with service.session.begin() as session:
        results = (
            session.query(model.Habitats)
            .filter(model.Habitats.habitat_id.in_(indice))
            .all()
        )
    return results


def get_habitat_by_id(habitat_id: int) -> model.Habitats:
    with service.session.begin() as session:
        result = (
            session.query(model.Habitats)
            .filter(model.Habitats.habitat_id == habitat_id)
            .first()
        )
    return result


def add_habitat(chinese_name: str, english_name: str) -> model.Habitats:
    new_habitat = model.Habitats(
        chinese_name=chinese_name,
        english_name=english_name,
    )
    with service.session.begin() as session:
        session.add(new_habitat)
        session.commit()
    return new_habitat
