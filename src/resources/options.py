import sys
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session


sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import engine
import src.model as model


class Positions(Resource):
    def get(self):
        with Session(engine) as session:
            results = session.query(
                model.Positions.position_id, model.Positions.name
            ).all()
        return [result._asdict() for result in results]


class Habitats(Resource):
    def get(self):
        with Session(engine) as session:
            results = session.query(
                model.Habitats.habitat_id,
                model.Habitats.chinese_name,
                model.Habitats.english_name,
            ).all()
        return [result._asdict() for result in results]


class Cameras(Resource):
    def get(self):
        with Session(engine) as session:
            results = session.query(
                model.Cameras.camera_id,
                model.Cameras.model_name,
            ).all()
        return [result._asdict() for result in results]


class Events(Resource):
    def get(self):
        with Session(engine) as session:
            results = session.query(
                model.Events.event_id,
                model.Events.chinese_name,
                model.Events.english_name,
            ).all()
        return [result._asdict() for result in results]


class Layers(Resource):
    def get(self):
        with Session(engine) as session:
            results = session.query(
                model.Layers.layer_id,
                model.Layers.name,
            ).all()
        return [result._asdict() for result in results]


class MountTypes(Resource):
    def get(self):
        with Session(engine) as session:
            results = session.query(
                model.MountTypes.mount_type_id,
                model.MountTypes.name,
            ).all()
        return [result._asdict() for result in results]


class Projects(Resource):
    def get(self):
        with Session(engine) as session:
            results = session.query(
                model.Projects.project_id,
                model.Projects.name,
            ).all()
        return [result._asdict() for result in results]
