import sys
from os.path import dirname
from sqlalchemy import func, and_, or_, desc
from sqlalchemy.orm import Session
from flask_restful import Resource, reqparse

sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import master_engine, slave_engine
import src.model as model


class PerchMounts(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = (
                session.query(
                    model.PerchMounts.perch_mount_id,
                    model.PerchMounts.perch_mount_name,
                    model.PerchMounts.latitude,
                    model.PerchMounts.longitude,
                    model.PerchMounts.terminated,
                    model.PerchMounts.latest_note,
                    model.PerchMounts.is_priority,
                    model.Habitats.habitat_id,
                    model.Habitats.chinese_name.label("habitat"),
                    model.Projects.project_id,
                    model.Projects.name.label("project"),
                    model.Layers.name.label("layer"),
                    model.Members.first_name.label("claim_by"),
                )
                .join(
                    model.Habitats,
                    model.Habitats.habitat_id == model.PerchMounts.habitat,
                    isouter=True,
                )
                .join(
                    model.Projects,
                    model.Projects.project_id == model.PerchMounts.project,
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
            ).all()
        return [result._asdict() for result in results]


class PerchMount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("perch_mount_name", type=str)
    parser.add_argument("longitude", type=float)
    parser.add_argument("latitude", type=float)
    parser.add_argument("habitat", type=int)
    parser.add_argument("project", type=int)
    parser.add_argument("layer", type=int)
    parser.add_argument("is_priority", type=bool)
    parser.add_argument("terminated", type=bool)

    layer_ref = {1: "上層", 2: "中層", 3: "下層"}

    def get(self, perch_mount_id: int):
        return self._get_perch_mount(perch_mount_id)

    def post(self):
        arg = self.parser.parse_args()

        perch_mount_name = arg.perch_mount_name

        if arg.layer:
            perch_mount_name += " %s" % self.layer_ref[int(arg.layer)]

        with Session(master_engine) as session:
            new_perch_mount = model.PerchMounts(
                perch_mount_name=perch_mount_name,
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

        with Session(master_engine) as session:
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
        with Session(slave_engine) as session:
            result = (
                session.query(
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
                .first()
            )

        return result._asdict() if result else None


class PerchMountClaimBy(Resource):
    def put(self, perch_mount_id: int, member_id: int):
        with Session(master_engine) as session:
            session.query(model.PerchMounts).filter(
                model.PerchMounts.perch_mount_id == perch_mount_id
            ).update({"claim_by": member_id})
            session.commit()

    def delete(self, perch_mount_id: int):
        with Session(master_engine) as session:
            session.query(model.PerchMounts).filter(
                model.PerchMounts.perch_mount_id == perch_mount_id
            ).update({"claim_by": None})
            session.commit()


class PendingPerchMounts(Resource):
    def get(self):
        with Session(slave_engine) as session:
            empty_count = (
                session.query(
                    func.count(model.EmptyMedia.empty_medium_id).label("count"),
                    model.Sections.perch_mount,
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.EmptyMedia.section,
                )
                .group_by(model.Sections.perch_mount)
                .filter(model.EmptyMedia.checked == 0)
                .subquery()
            )
            detected_count = (
                session.query(
                    func.count(model.DetectedMedia.detected_medium_id).label("count"),
                    model.Sections.perch_mount,
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.DetectedMedia.section,
                )
                .group_by(model.Sections.perch_mount)
                .filter(model.DetectedMedia.reviewed == 0)
                .subquery()
            )
            results = (
                session.query(
                    model.PerchMounts.perch_mount_id,
                    model.PerchMounts.perch_mount_name,
                    model.PerchMounts.is_priority,
                    model.PerchMounts.project.label("project_id"),
                    model.Members.first_name.label("claim_by"),
                    model.Projects.name.label("project"),
                    empty_count.c.count.label("empty_count"),
                    detected_count.c.count.label("detected_count"),
                    model.PerchMounts.latest_note,
                )
                .join(
                    empty_count,
                    empty_count.c.perch_mount == model.PerchMounts.perch_mount_id,
                    isouter=True,
                )
                .join(
                    detected_count,
                    detected_count.c.perch_mount == model.PerchMounts.perch_mount_id,
                    isouter=True,
                )
                .join(
                    model.Members,
                    model.Members.member_id == model.PerchMounts.claim_by,
                    isouter=True,
                )
                .join(
                    model.Projects,
                    model.Projects.project_id == model.PerchMounts.project,
                    isouter=True,
                )
                .filter(or_(empty_count.c.count > 0, detected_count.c.count > 0))
                .all()
            )
        return [result._asdict() for result in results]


class ClaimedPerchMounts(Resource):
    def get(self, member_id: int):
        with Session(slave_engine) as session:
            results = (
                session.query(
                    model.PerchMounts.perch_mount_id,
                    model.PerchMounts.perch_mount_name,
                    model.PerchMounts.is_priority,
                    model.PerchMounts.latest_note,
                    model.PerchMounts.habitat.label("habitat_id"),
                    model.PerchMounts.project.label("project_id"),
                    model.Habitats.chinese_name.label("habitat"),
                    model.Projects.name.label("project"),
                    model.Layers.name.label("layer"),
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
                .filter(model.PerchMounts.claim_by == member_id)
                .all()
            )
        return [result._asdict() for result in results]


class PerchMountMediaCount(Resource):
    def get(self, perch_mount_id: int):
        with Session(slave_engine) as session:
            count = (
                session.query(func.count(model.Media.medium_id))
                .join(model.Sections, model.Sections.section_id == model.Media.section)
                .filter(model.Sections.perch_mount == perch_mount_id)
                .one()
            )[0]
            detected_count = (
                session.query(func.count(model.DetectedMedia.detected_medium_id))
                .join(
                    model.Sections,
                    model.Sections.section_id == model.DetectedMedia.section,
                )
                .filter(
                    and_(
                        model.Sections.perch_mount == perch_mount_id,
                        model.DetectedMedia.reviewed == 0,
                    )
                )
                .one()
            )[0]
            empty_count = (
                session.query(func.count(model.EmptyMedia.empty_medium_id))
                .join(
                    model.Sections,
                    model.Sections.section_id == model.EmptyMedia.section,
                )
                .filter(
                    and_(
                        model.Sections.perch_mount == perch_mount_id,
                        model.EmptyMedia.checked == 0,
                    )
                )
                .one()
            )[0]
        return {
            "count": count,
            "detected_count": detected_count,
            "empty_count": empty_count,
        }


class PerchMountMonthPendingEmptyCount(Resource):
    def get(self, perch_mount_id):
        with Session(slave_engine) as session:
            results = (
                session.query(
                    func.count(model.EmptyMedia.empty_medium_id).label("count"),
                    func.date_format(model.EmptyMedia.medium_datetime, "%Y-%m").label(
                        "year_month"
                    ),
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.EmptyMedia.section,
                )
                .group_by(
                    func.date_format(model.EmptyMedia.medium_datetime, "%Y-%m"),
                    model.Sections.perch_mount,
                )
                .filter(
                    model.EmptyMedia.checked == 0,
                    model.Sections.perch_mount == perch_mount_id,
                )
                .order_by(
                    desc(func.date_format(model.EmptyMedia.medium_datetime, "%Y-%m"))
                )
                .all()
            )

        return [result._asdict() for result in results]


class PerchMountMonthPendingDetectedCount(Resource):
    def get(self, perch_mount_id):
        with Session(slave_engine) as session:
            reviewed = (
                session.query(
                    func.count(model.Media.medium_id).label("count"),
                    func.date_format(model.Media.medium_datetime, "%Y-%m").label(
                        "year_month"
                    ),
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.Media.section,
                )
                .group_by(func.date_format(model.Media.medium_datetime, "%Y-%m"))
                .filter(model.Sections.perch_mount == perch_mount_id)
                .subquery()
            )
            detected = (
                session.query(
                    func.count(model.DetectedMedia.detected_medium_id).label("count"),
                    func.date_format(
                        model.DetectedMedia.medium_datetime, "%Y-%m"
                    ).label("year_month"),
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.DetectedMedia.section,
                )
                .group_by(
                    func.date_format(model.DetectedMedia.medium_datetime, "%Y-%m")
                )
                .filter(
                    and_(
                        model.DetectedMedia.reviewed == 0,
                        model.Sections.perch_mount == perch_mount_id,
                    )
                )
                .order_by(
                    desc(func.date_format(model.DetectedMedia.medium_datetime, "%Y-%m"))
                )
                .subquery()
            )

            results = (
                session.query(
                    detected.c.year_month,
                    detected.c.count,
                    reviewed.c.count.label("reviewed_count"),
                )
                .join(
                    reviewed,
                    reviewed.c.year_month == detected.c.year_month,
                    isouter=True,
                )
                .all()
            )
        return [result._asdict() for result in results]
