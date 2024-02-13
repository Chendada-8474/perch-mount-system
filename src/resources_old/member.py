import sys
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import master_engine, slave_engine
import src.model as model


class AllMembers(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = (
                session.query(
                    model.Members.member_id,
                    model.Members.user_name,
                    model.Members.phone_number,
                    model.Members.first_name,
                    model.Members.last_name,
                    model.Members.is_admin,
                    model.Members.is_super_admin,
                    model.Positions.name.label("position"),
                )
                .join(
                    model.Positions,
                    model.Positions.position_id == model.Members.position,
                )
                .order_by(model.Members.member_id)
                .all()
            )
        return [result._asdict() for result in results]


class Member(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("user_name", type=str)
    parser.add_argument("phone_number", type=str)
    parser.add_argument("first_name", type=str)
    parser.add_argument("last_name", type=str)
    parser.add_argument("position", type=int)
    parser.add_argument("is_admin", type=bool)

    def get(self, member_id: int):
        return self._get_member_by_id(member_id)

    def post(self):
        arg = self.parser.parse_args()
        with Session(master_engine) as session:
            new_member = model.Members(
                user_name=arg.user_name,
                phone_number=arg.phone_number,
                first_name=arg.first_name,
                last_name=arg.last_name,
                position=arg.position,
            )
            session.add(new_member)
            session.commit()
            new_member_id = new_member.member_id
        return self._get_member_by_id(new_member_id)

    def patch(self, member_id: int):
        arg = self.parser.parse_args()
        with Session(master_engine) as session:
            session.query(model.Members).filter(
                model.Members.member_id == member_id
            ).update(dict(arg))
            session.commit()
        return self._get_member_by_id(member_id)

    def _get_member_by_id(self, member_id):
        with Session(slave_engine) as session:
            result = (
                session.query(
                    model.Members.member_id,
                    model.Members.user_name,
                    model.Members.phone_number,
                    model.Members.first_name,
                    model.Members.last_name,
                    model.Members.is_admin,
                    model.Members.is_super_admin,
                    model.Positions.name.label("position"),
                )
                .join(
                    model.Positions,
                    model.Positions.position_id == model.Members.position,
                    isouter=True,
                )
                .filter(model.Members.member_id == member_id)
                .one()
            )
        return result._asdict()


class MemberContributions(Resource):
    def get(self, member_id: int):
        with Session(slave_engine) as session:
            reviews = (
                session.query(func.sum(model.Contributions.num_files).label("count"))
                .filter(
                    and_(
                        model.Contributions.action == 2,
                        model.Contributions.contributor == member_id,
                    )
                )
                .one()
            )
            checks = (
                session.query(func.sum(model.Contributions.num_files).label("count"))
                .filter(
                    and_(
                        model.Contributions.action == 1,
                        model.Contributions.contributor == member_id,
                    )
                )
                .one()
            )
            operations = (
                session.query(func.count(model.SectionOperators.section).label("count"))
                .filter(model.SectionOperators.operator == member_id)
                .one()
            )
        result = {
            "reviews": int(reviews.count) if reviews.count else None,
            "checks": int(checks.count) if checks.count else None,
            "operations": int(operations.count) if operations.count else None,
        }
        return result
