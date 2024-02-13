import service
from src import model


def get_layers() -> list[model.Layers]:
    with service.session.begin() as session:
        results = session.query(model.Layers).all()
    return results


def get_layer_by_id(layer_id: int) -> model.Layers:
    with service.session.begin() as session:
        result = (
            session.query(model.Layers).filter(model.Layers.layer_id == layer_id).one()
        )
    return result


def add_layer(name: str) -> model.Layers:
    new_layer = model.Layers(name=name)
    with service.session.begin() as session:
        session.add(new_layer)
        session.commit()
    return new_layer
