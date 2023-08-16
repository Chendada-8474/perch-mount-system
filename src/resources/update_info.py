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
    parser.add_argument("checked", type=bool)

    def get(self, update_info_id: int):
        with Session(slave_engine) as session:
            result = (
                session.query(
                    model.UpdateInfo.detail,
                    func.date_format(model.UpdateInfo.create_date, "%Y-%m-%d").label(
                        "create_date"
                    ),
                )
                .filter(model.UpdateInfo.update_info_id == update_info_id)
                .one()
            )
        return result._asdict()

    def post(self):
        new_update_info = model.UpdateInfo(
            message_file_name=datetime.today().strftime("%Y%m%d_mes.md"),
            detail_file_name=datetime.today().strftime("%Y%m%d_detail.md"),
        )
        with Session(master_engine) as session:
            session.add(new_update_info)
            session.commit()

    def patch(self, update_info_id: int):
        arg = self.parser.parse_args()

        with Session(master_engine) as session:
            session.query(model.UpdateInfo).filter(
                model.UpdateInfo.update_info_id == update_info_id
            ).update(dict(arg))
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
