import sys
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import engine
import src.model as model


class SectionsOfPerchMount(Resource):
    def get(self, perch_mount_id: int):
        with Session(engine) as session:
            detected_count = (
                session.query(
                    model.DetectedMedia.section,
                    func.count(model.DetectedMedia.detected_medium_id).label("count"),
                )
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
                .group_by(model.DetectedMedia.section)
                .subquery()
            )
            empty_count = (
                session.query(
                    model.EmptyMedia.section,
                    func.count(model.EmptyMedia.empty_medium_id).label("count"),
                )
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
                .group_by(model.EmptyMedia.section)
                .subquery()
            )
            results = (
                (
                    session.query(
                        model.Sections.section_id,
                        func.date_format(
                            model.Sections.start_time, "%Y-%m-%d %H:%i:%S"
                        ).label("start_time"),
                        func.date_format(
                            model.Sections.end_time, "%Y-%m-%d %H:%i:%S"
                        ).label("end_time"),
                        func.date_format(model.Sections.check_date, "%Y-%m-%d").label(
                            "check_date"
                        ),
                        model.Sections.valid,
                        model.PerchMounts.perch_mount_name,
                        model.MountTypes.name.label("mount_type"),
                        model.Cameras.model_name.label("model_name"),
                        model.Members.first_name,
                        model.Sections.note,
                        detected_count.c.count.label("detected_count"),
                        empty_count.c.count.label("empty_count"),
                    )
                    .join(
                        model.PerchMounts,
                        model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
                        isouter=True,
                    )
                    .join(
                        model.MountTypes,
                        model.MountTypes.mount_type_id == model.Sections.mount_type,
                        isouter=True,
                    )
                    .join(
                        model.Cameras,
                        model.Cameras.camera_id == model.Sections.camera,
                        isouter=True,
                    )
                    .join(
                        model.SectionOperators,
                        model.SectionOperators.section == model.Sections.section_id,
                        isouter=True,
                    )
                    .join(
                        model.Members,
                        model.Members.member_id == model.SectionOperators.operator,
                        isouter=True,
                    )
                    .join(
                        detected_count,
                        detected_count.c.section == model.Sections.section_id,
                        isouter=True,
                    )
                    .join(
                        empty_count,
                        empty_count.c.section == model.Sections.section_id,
                        isouter=True,
                    )
                )
                .order_by(model.Sections.section_id)
                .filter(model.Sections.perch_mount == perch_mount_id)
                .all()
            )

        section_id = 0
        new_results = []
        for result in results:
            if result.section_id != section_id:
                new_result = {
                    "section_id": result.section_id,
                    "start_time": result.start_time,
                    "end_time": result.end_time,
                    "check_date": result.check_date,
                    "valid": result.valid,
                    "perch_mount_name": result.perch_mount_name,
                    "mount_type": result.mount_type,
                    "model_name": result.model_name,
                    "note": result.note,
                    "detected_count": result.detected_count,
                    "empty_count": result.empty_count,
                    "operators": [],
                }
                new_results.append(new_result)
                section_id = result.section_id
            new_results[-1]["operators"].append(result.first_name)

        return new_results


class OperatorsOfSection(Resource):
    def get(self, section_id: int):
        with Session(engine) as session:
            results = (
                session.query(
                    model.SectionOperators.section,
                    model.Members.member_id,
                    model.Members.first_name,
                )
                .join(
                    model.Members,
                    model.Members.member_id == model.SectionOperators.operator,
                )
                .filter(model.SectionOperators.section == section_id)
                .all()
            )
        return [result._asdict() for result in results]


class OneSection(Resource):
    def get(self, section_id: int):
        with Session(engine) as session:
            result = (
                session.query(
                    model.Sections.section_id,
                    model.Sections.perch_mount.label("perch_mount_id"),
                    model.PerchMounts.perch_mount_name.label("perch_mount_name"),
                    func.date_format(
                        model.Sections.start_time, "%Y-%m-%d %H:%i:%S"
                    ).label("start_time"),
                    func.date_format(
                        model.Sections.end_time, "%Y-%m-%d %H:%i:%S"
                    ).label("end_time"),
                    func.date_format(model.Sections.check_date, "%Y-%m-%d").label(
                        "check_date"
                    ),
                    model.Sections.valid,
                    model.Sections.note,
                    model.MountTypes.name.label("mount_type"),
                    model.Cameras.model_name.label("camera"),
                )
                .join(
                    model.MountTypes,
                    model.MountTypes.mount_type_id == model.Sections.mount_type,
                    isouter=True,
                )
                .join(
                    model.Cameras,
                    model.Cameras.camera_id == model.Sections.camera,
                    isouter=True,
                )
                .join(
                    model.PerchMounts,
                    model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
                    isouter=True,
                )
                .filter(model.Sections.section_id == section_id)
                .one()
            )
        return result._asdict()
