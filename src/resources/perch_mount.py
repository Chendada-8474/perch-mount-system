import sys
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session

sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import engine
import src.model as model


class PerchMount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("perch_mount_name", type=str)
    parser.add_argument("longitude", type=float)
    parser.add_argument("latitude", type=float)
    parser.add_argument("habitat", type=int)
    parser.add_argument("project", type=int)
    parser.add_argument("layer", type=int)
    parser.add_argument("latest_note", type=str)
    parser.add_argument("claim_by", type=int)
    parser.add_argument("is_priority", type=bool)

    def get(self, perch_mount_id: int):
        return self._get_perch_mount(perch_mount_id)

    def post(self):
        arg = self.parser.parse_args()

        with Session(engine) as session:
            new_perch_mount = model.PerchMounts(
                perch_mount_name=arg.perch_mount_name,
                longitude=arg.longitude,
                latitude=arg.latitude,
                habitat=arg.habitat,
                project=arg.project,
                layer=arg.layer,
            )
            session.add(new_perch_mount)
            session.commit()
            new_perch_mount_id = new_perch_mount.perch_mount_id

        return self._get_perch_mount(new_perch_mount_id)

    def patch(self, perch_mount_id: int):
        arg = self.parser.parse_args()

        if arg.perch_mount_name:
            return {"message": "updating perch_mount_name is not allowed."}

        arg = self._pop_null_column(dict(arg))

        with Session(engine) as session:
            session.query(model.PerchMounts).filter(
                model.PerchMounts.perch_mount_id == perch_mount_id
            ).update(arg)
            session.commit()

        return self._get_perch_mount(perch_mount_id)

    def _pop_null_column(self, arg: dict):
        cols = []
        for k, v in arg.items():
            if v == None:
                cols.append(k)
        for c in cols:
            arg.pop(c)
        return arg

    def _get_perch_mount(self, perch_mount_id: int) -> dict:
        with Session(engine) as session:
            query = (
                model.PerchMounts.query.with_entities(
                    model.PerchMounts.perch_mount_id,
                    model.PerchMounts.perch_mount_name,
                    model.PerchMounts.latitude,
                    model.PerchMounts.longitude,
                    model.PerchMounts.latest_note,
                    model.PerchMounts.terminated,
                    model.PerchMounts.is_priority,
                    model.Habitats.chinese_name.label("habitat"),
                    model.Projects.name.label("project"),
                    model.Layers.name.label("layer"),
                    model.Members.user_name.label("claim_by"),
                )
                .join(
                    model.Habitats,
                    model.Habitats.habitat_id == model.PerchMounts.habitat,
                    isouter=True,
                )
                .join(
                    model.Projects,
                    model.Projects.project_id == model.PerchMounts.project,
                    isouter=True,
                )
                .join(
                    model.Layers,
                    model.Layers.layer_id == model.PerchMounts.layer,
                    isouter=True,
                )
                .join(
                    model.Members,
                    model.Members.member_id == model.PerchMounts.claim_by,
                    isouter=True,
                )
                .filter(model.PerchMounts.perch_mount_id == perch_mount_id)
            )
            result = session.execute(query).one()
        return result._asdict()


class PendingPerchMounts(Resource):
    def get(self):
        return


class ClaimedPerchMounts(Resource):
    def get(self, member_id: int):
        with Session(engine) as session:
            results = (
                session.query(
                    model.PerchMounts.perch_mount_id, model.PerchMounts.perch_mount_name
                )
                .filter(model.PerchMounts.claim_by == member_id)
                .all()
            )
        return [result._asdict() for result in results]
