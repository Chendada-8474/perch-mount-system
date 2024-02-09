import sys
from os.path import dirname
from datetime import datetime
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import master_engine, slave_engine
import src.model as model


class UpdateInfo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("message", type=str)
    parser.add_argument("detail", type=str)

    def get(self, update_info_id: int):
        with Session(slave_engine) as session:
            result = (
                session.query(
                    model.UpdateInfo.detail,
                    model.UpdateInfo.message,
                    func.date_format(model.UpdateInfo.create_date, "%Y-%m-%d").label(
                        "create_date"
                    ),
                )
                .filter(model.UpdateInfo.update_info_id == update_info_id)
                .one()
            )
        return result._asdict()

    def post(self):
        arg = self.parser.parse_args()
        new_update_info = model.UpdateInfo(
            message_file_name=arg.message,
            detail_file_name=arg.detail,
        )
        with Session(master_engine) as session:
            session.add(new_update_info)
            session.commit()

    def delete(self, update_info_id: int):
        with Session(master_engine) as session:
            session.query(model.UpdateInfo).filter(
                model.UpdateInfo.update_info_id == update_info_id
            ).update({"checked": True})
            session.commit()


class UpdateInfos(Resource):
    def get(self):
        with Session(slave_engine) as session:
            results = (
                session.query(
                    model.UpdateInfo.update_info_id,
                    model.UpdateInfo.message,
                    model.UpdateInfo.detail,
                    model.UpdateInfo.checked,
                    func.date_format(model.UpdateInfo.create_date, "%Y-%m-%d").label(
                        "create_date"
                    ),
                )
                .order_by(desc(model.UpdateInfo.create_date))
                .limit(10)
                .all()
            )
        return [result._asdict() for result in results]
