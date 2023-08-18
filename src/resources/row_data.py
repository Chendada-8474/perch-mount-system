import sys
import ast
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import slave_engine
import src.model as model
import configs.config as config


class RowData(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("project", action="append")
    parser.add_argument("perch_mount", action="append")
    parser.add_argument("species", action="append")
    parser.add_argument("raptor", type=int)
    parser.add_argument("start_time", type=str)
    parser.add_argument("end_time", type=str)
    parser.add_argument("prey", type=bool)
    parser.add_argument("tagged", type=bool)
    parser.add_argument("identified_prey", type=bool)

    def post(self):
        arg = self.parser.parse_args()

        conditions = self._prase_conditions(arg)
        return self._get_data(conditions)

    def _prase_conditions(self, arg):
        conditions = []
        if arg.project:
            conditions.append(model.PerchMounts.project.in_(arg.project))

        if arg.perch_mount:
            conditions.append(model.Sections.perch_mount.in_(arg.perch_mount))

        if arg.species:
            conditions.append(model.Species.taxon_order.in_(arg.species))

        if arg.raptor:
            conditions.append(
                model.Species.order.in_(config.RAPTOR_ORDERS)
                if int(arg.raptor) == 1
                else ~model.Species.order.in_(config.RAPTOR_ORDERS)
            )

        if arg.start_time:
            conditions.append(model.Media.medium_datetime >= arg.start_time)

        if arg.end_time:
            conditions.append(model.Media.medium_datetime <= arg.end_time)

        if arg.prey:
            conditions.append(model.Individuals.prey == True)

        if arg.identified_prey:
            conditions.append(model.Individuals.prey_name != None)

        if arg.tagged:
            conditions.append(model.Individuals.tagged == True)

        return conditions

    def _get_data(self, conditions: list):
        with Session(slave_engine) as session:
            row_data = (
                session.query(
                    model.Species.taxon_order,
                    model.Species.chinese_common_name.label("species"),
                    model.Individuals.prey_name,
                    model.Individuals.prey,
                    func.date_format(
                        model.Media.medium_datetime, "%Y-%m-%d %H:%i:%S"
                    ).label("medium_datetime"),
                    model.Individuals.ring_number,
                    model.Individuals.tagged,
                    model.PerchMounts.perch_mount_name.label("perch_mount"),
                    model.Projects.name.label("project"),
                )
                .join(
                    model.Species,
                    model.Species.taxon_order == model.Individuals.taxon_order_by_human,
                    isouter=True,
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
                .join(
                    model.PerchMounts,
                    model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
                    isouter=True,
                )
                .join(
                    model.Projects,
                    model.Projects.project_id == model.PerchMounts.project,
                    isouter=True,
                )
                .filter(and_(*conditions))
                .subquery()
            )

            species = (
                session.query(
                    row_data.c.species,
                    model.Species.scientific_name,
                    model.Species.english_common_name,
                    model.Species.family_latin_name,
                    model.Species.taiwan_status,
                    model.Species.endemism,
                    model.Species.conservation_status,
                )
                .join(
                    model.Species,
                    model.Species.taxon_order == row_data.c.taxon_order,
                    isouter=True,
                )
                .group_by(model.Species.taxon_order)
                .all()
            )

            results = session.query(row_data).all()

        return {
            "row_data": [result._asdict() for result in results],
            "species_list": [sp._asdict() for sp in species],
        }
