import sys
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc

sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import master_engine, slave_engine
import src.model as model


class PerchMountSectionPreyCount(Resource):
    def get(self, perch_mount_id: int):
        with Session(slave_engine) as session:
            indentidied = (
                session.query(
                    func.count(model.Individuals.individual_id).label("count"),
                    model.Media.section,
                )
                .join(
                    model.Media,
                    model.Media.medium_id == model.Individuals.medium,
                    isouter=True,
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.Media.section,
                    isouter=True,
                )
                .filter(model.Sections.perch_mount == perch_mount_id)
                .filter(
                    model.Individuals.prey, model.Individuals.prey_name.is_not(None)
                )
                .group_by(model.Media.section)
                .subquery()
            )
            results = (
                session.query(
                    func.count(model.Individuals.individual_id).label("prey_count"),
                    indentidied.c.count.label("identified_count"),
                    model.Media.section,
                    func.date_format(model.Sections.check_date, "%Y-%m-%d").label(
                        "check_date"
                    ),
                )
                .join(
                    model.Media,
                    model.Media.medium_id == model.Individuals.medium,
                    isouter=True,
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.Media.section,
                    isouter=True,
                )
                .filter(model.Sections.perch_mount == perch_mount_id)
                .filter(or_(model.Individuals.prey, model.Individuals.prey_name))
                .group_by(model.Media.section)
                .order_by(
                    desc(model.Sections.check_date),
                    func.date_format(model.Sections.check_date, "%Y-%m-%d"),
                )
                .join(
                    indentidied,
                    indentidied.c.section == model.Media.section,
                    isouter=True,
                )
                .all()
            )
        return [result._asdict() for result in results]


class IdentifySectionPreys(Resource):
    def get(self, section_id: int):
        with Session(slave_engine) as session:
            results = (
                session.query(
                    model.Media.medium_id,
                    model.Media.path,
                    model.Individuals.individual_id,
                    model.Individuals.prey_name,
                    model.Species.chinese_common_name,
                )
                .join(
                    model.Individuals,
                    model.Individuals.medium == model.Media.medium_id,
                    isouter=True,
                )
                .join(
                    model.Species,
                    model.Species.taxon_order == model.Individuals.taxon_order_by_human,
                    isouter=True,
                )
                .filter(model.Media.section == section_id)
                .filter(or_(model.Individuals.prey, model.Individuals.prey_name))
                .order_by(model.Media.medium_datetime)
                .all()
            )

            media = []
            medium_id = ""
            for result in results:
                if not result.individual_id:
                    continue
                if result.medium_id != medium_id:
                    media.append(
                        {
                            "medium_id": result.medium_id,
                            "path": result.path,
                            "individuals": [],
                        }
                    )
                    medium_id = result.medium_id

                media[-1]["individuals"].append(
                    {
                        "individual_id": result.individual_id,
                        "prey_name": result.prey_name,
                        "predator": result.chinese_common_name,
                    }
                )
        return media


class Prey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("prey_name", type=str)
    parser.add_argument("prey_identify_by", type=int)

    def put(self, individual_id: int):
        arg = self.parser.parse_args()
        update = {
            "prey": arg.prey_name != None,
            "prey_name": arg.prey_name,
            "prey_identify_by": arg.prey_identify_by if arg.prey_name else None,
        }

        with Session(master_engine) as session:
            session.query(model.Individuals).filter(
                model.Individuals.individual_id == individual_id
            ).update(update)
            session.commit()
