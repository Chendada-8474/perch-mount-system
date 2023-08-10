import sys
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session
from sqlalchemy import func, select

sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import master_engine
import src.model as model


class IndividualsOfMedium(Resource):
    def get(self, medium_id: int):
        species_human = select(model.Species)
        with Session(master_engine) as session:
            results = (
                session.query(
                    model.Individuals.individual_id,
                    model.Individuals.prey,
                    model.Individuals.prey_name,
                    model.Individuals.tagged,
                    model.Individuals.ring_number,
                    model.Individuals.xmin,
                    model.Individuals.xmax,
                    model.Individuals.ymin,
                    model.Individuals.ymax,
                    model.Species.chinese_common_name.label("ai_species"),
                    species_human.c.chinese_common_name.label("species"),
                )
                .join(
                    model.Species,
                    model.Species.taxon_order == model.Individuals.taxon_order_by_ai,
                    isouter=True,
                )
                .join(
                    species_human,
                    species_human.c.taxon_order
                    == model.Individuals.taxon_order_by_human,
                    isouter=True,
                )
                .filter(model.Individuals.medium == medium_id)
                .all()
            )
        return [result._asdict() for result in results]


class Individual(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("taxon_order_by_human", type=int)
    parser.add_argument("prey", type=bool)
    parser.add_argument("prey_name", type=str)
    parser.add_argument("tagged", type=bool)
    parser.add_argument("ring_number", type=str)

    def post(self, medium_id: str):
        arg = self.parser.parse_args()
        new_individual = model.Individuals(
            medium=medium_id,
            taxon_order_by_human=arg.taxon_order_by_human,
        )

        with Session(master_engine) as session:
            session.add(new_individual)
            session.commit()

    def patch(self, individual_id: int):
        arg = self.parser.parse_args()
        print(dict(arg))

        with Session(master_engine) as session:
            session.query(model.Individuals).filter(
                model.Individuals.individual_id == individual_id
            ).update(dict(arg))
            session.commit()

        return self._get_individual_by_id(individual_id)

    def delete(self, individual_id: int):
        with Session(master_engine) as session:
            session.query(model.Individuals).filter(
                model.Individuals.individual_id == individual_id
            ).delete()
            session.commit()

    def _get_individual_by_id(self, individual_id):
        with Session(master_engine) as session:
            result = (
                session.query(
                    model.Individuals.individual_id,
                    model.Individuals.prey,
                    model.Individuals.prey_name,
                    model.Individuals.ring_number,
                    model.Species.chinese_common_name,
                )
                .join(
                    model.Species,
                    model.Species.taxon_order == model.Individuals.taxon_order_by_human,
                )
                .filter(model.Individuals.individual_id == individual_id)
                .one()
            )
        return result._asdict()
