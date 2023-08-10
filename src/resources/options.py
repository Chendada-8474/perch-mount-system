import sys
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session


sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import master_engine, slave_engine
from src.species import SpeciesTrie, SpeciesNames
import src.model as model


class Positions(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.Positions.position_id, model.Positions.name
            ).all()
        return [result._asdict() for result in results]


class Habitats(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.Habitats.habitat_id,
                model.Habitats.chinese_name,
                model.Habitats.english_name,
            ).all()
        return [result._asdict() for result in results]


class AllCameras(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.Cameras.camera_id,
                model.Cameras.model_name,
            ).all()
        return [result._asdict() for result in results]


class AllEvents(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.Events.event_id,
                model.Events.chinese_name,
                model.Events.english_name,
            ).all()
        return [result._asdict() for result in results]


class Layers(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.Layers.layer_id,
                model.Layers.name,
            ).all()
        return [result._asdict() for result in results]


class MountTypes(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.MountTypes.mount_type_id,
                model.MountTypes.name,
            ).all()
        return [result._asdict() for result in results]


class Projects(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.Projects.project_id,
                model.Projects.name,
            ).all()
        return [result._asdict() for result in results]


class AllBehaviors(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.Behaviors.behavior_id, model.Behaviors.chinese_name
            ).all()
        return [result._asdict() for result in results]


class Behavior(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("chinese_name", type=str)

    def post(self):
        arg = self.parser.parse_args()
        new_behavior = model.Behaviors(chinese_name=arg.chinese_name)
        with Session(master_engine) as session:
            session.add(new_behavior)
            session.commit()


class Camera(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("model_name", type=str)

    def post(self):
        arg = self.parser.parse_args()
        new_camera = model.Cameras(model_name=arg.model_name)
        with Session(master_engine) as session:
            session.add(new_camera)
            session.commit()


class Event(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("chinese_name", type=str)
    parser.add_argument("english_name", type=str)

    def post(self):
        arg = self.parser.parse_args()
        new_event = model.Events(
            chinese_name=arg.chinese_name,
            english_name=arg.english_name,
        )
        with Session(master_engine) as session:
            session.add(new_event)
            session.commit()


class AllSpecies(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.Species.taxon_order,
                model.Species.chinese_common_name,
                model.Species.english_common_name,
                model.Species.scientific_name,
                model.Species.family_name,
                model.Species.taiwan_status,
                model.Species.conservation_status,
                model.Species.endemism,
            ).all()
        return [result._asdict() for result in results]


class SpeciesTrie(Resource):
    trie = SpeciesTrie()

    def get(self, word: str = None):
        return self.trie.search(word)


class SpeciesTaxonOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("chinese_common_names", action="append")

    species_names = SpeciesNames()

    def post(self):
        arg = self.parser.parse_args()
        if not arg.chinese_common_names:
            return []
        return self.species_names.get_taxon_orders(arg.chinese_common_names)
