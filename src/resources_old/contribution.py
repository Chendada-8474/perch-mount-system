import sys
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session

sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import master_engine
import src.model as model


class Contribution(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("contributor", type=int)
    parser.add_argument("num_files", type=int)
    parser.add_argument("action", type=int)
    parser.add_argument("time", type=str)

    def post(self):
        arg = self.parser.parse_args()
        new_contibution = model.Contributions(
            contributor=arg.contributor,
            num_files=arg.num_files,
            action=arg.action,
            time=arg.time,
        )
        with Session(master_engine) as session:
            session.add(new_contibution)
            session.commit()


class ScheduleDetectCount(Resource):
    def post(self, section_id: int, num_files: int, is_image: int):
        new_detection = model.ScheduleDetect(
            num_files=num_files,
            section=section_id,
            is_image=is_image != 0,
        )
        with Session(master_engine) as session:
            session.add(new_detection)
            session.commit()
