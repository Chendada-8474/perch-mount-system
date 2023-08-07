import sys
import ast
from os.path import dirname
from flask_restful import Resource, reqparse
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, and_, select


sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import engine
import src.model as model
import src.file as file


class Medium(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("event", type=int)
    parser.add_argument("featured", type=bool)
    parser.add_argument("featured_by", type=int)

    def get(self, medium_id: str):
        return self._get_medium_by_id(medium_id)

    def patch(self, medium_id):
        arg = self.parser.parse_args()

        with Session(engine) as session:
            session.query(model.Media).filter(
                model.Media.medium_id == medium_id
            ).update(dict(arg))
            session.commit()

        return self._get_medium_by_id(medium_id)

    def _get_medium_by_id(self, medium_id: str):
        reviewer = aliased(model.Members)
        featured_by = aliased(model.Members)

        with Session(engine) as session:
            result = (
                (
                    session.query(
                        model.Media.medium_id,
                        model.Media.section,
                        func.date_format(
                            model.Media.medium_datetime, "%Y-%m-%d %H:%i:%S"
                        ).label("medium_datetime"),
                        model.Media.path,
                        model.Media.featured,
                        model.Events.chinese_name.label("event"),
                        reviewer.first_name.label("reviewer"),
                        featured_by.first_name.label("featured_by"),
                    )
                    .join(
                        reviewer,
                        reviewer.member_id == model.Media.reviewer,
                        isouter=True,
                    )
                    .join(
                        featured_by,
                        featured_by.member_id == model.Media.featured_by,
                        isouter=True,
                    )
                    .join(
                        model.Events,
                        model.Events.event_id == model.Media.event,
                        isouter=True,
                    )
                )
                .filter(model.Media.medium_id == medium_id)
                .one()
            )

        return result._asdict()


class SectionMedia(Resource):
    def get(self, section_id: int):
        empty_checker = aliased(model.Members)

        with Session(engine) as session:
            results = (
                session.query(
                    model.Media.medium_id,
                    model.Media.section,
                    func.date_format(
                        model.Media.medium_datetime, "%Y-%m-%d %H:%i:%S"
                    ).label("medium_datetime"),
                    model.Media.path,
                    model.Media.featured_behavior,
                    model.Members.first_name.label("reviewer"),
                    empty_checker.first_name.label("empty_checker"),
                    model.Events.chinese_name.label("event"),
                )
                .join(
                    model.Members,
                    model.Members.member_id == model.Media.reviewer,
                    isouter=True,
                )
                .join(
                    model.Events,
                    model.Events.event_id == model.Media.event,
                    isouter=True,
                )
                .join(
                    empty_checker,
                    empty_checker.member_id == model.Media.empty_checker,
                    isouter=True,
                )
                .filter(model.Media.section == section_id)
            ).all()
        return [result._asdict() for result in results]


class SectionEmptyMedia(Resource):
    def get(self, section_id: int):
        with Session(engine) as session:
            results = (
                session.query(
                    model.EmptyMedia.empty_medium_id,
                    model.EmptyMedia.section,
                    func.date_format(
                        model.EmptyMedia.medium_datetime, "%Y-%m-%d %H:%i:%S"
                    ).label("medium_datetime"),
                )
                .filter(
                    and_(
                        model.EmptyMedia.section == section_id,
                        model.EmptyMedia.checked == 0,
                    )
                )
                .all()
            )
        return [result._asdict() for result in results]


class SectionDetectedMedia(Resource):
    def get(self, section_id: int):
        with Session(engine) as session:
            results = (
                session.query(
                    model.DetectedMedia.detected_medium_id,
                    model.DetectedMedia.section,
                    func.date_format(
                        model.DetectedMedia.medium_datetime, "%Y-%m-%d %H:%i:%S"
                    ).label("medium_datetime"),
                    model.Members.first_name.label("empty_checker"),
                )
                .join(
                    model.Members,
                    model.Members.member_id == model.DetectedMedia.empty_checker,
                    isouter=True,
                )
                .filter(
                    and_(
                        model.DetectedMedia.section == section_id,
                        model.DetectedMedia.reviewed == 0,
                    )
                )
                .all()
            )
        return [result._asdict() for result in results]


class EmptyDayCountOfPerchMount(Resource):
    def get(self, perch_mount_id: int):
        with Session(engine) as session:
            results = (
                session.query(
                    func.date_format(
                        model.EmptyMedia.medium_datetime, "%Y-%m-%d"
                    ).label("date"),
                    func.count().label("count"),
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.EmptyMedia.section,
                    isouter=True,
                )
                .filter(
                    and_(
                        model.Sections.perch_mount == perch_mount_id,
                        model.EmptyMedia.checked == False,
                    )
                )
                .group_by(
                    func.date_format(model.EmptyMedia.medium_datetime, "%Y-%m-%d")
                )
            ).all()

        return {
            "date": [result.date for result in results],
            "count": [result.count for result in results],
        }


class DetectedDayCountOfPerchMount(Resource):
    def get(self, perch_mount_id: int):
        with Session(engine) as session:
            results = (
                session.query(
                    func.date_format(
                        model.DetectedMedia.medium_datetime, "%Y-%m-%d"
                    ).label("date"),
                    func.count().label("count"),
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.DetectedMedia.section,
                    isouter=True,
                )
                .filter(
                    and_(
                        model.Sections.perch_mount == perch_mount_id,
                        model.DetectedMedia.reviewed == False,
                    )
                )
                .group_by(
                    func.date_format(model.DetectedMedia.medium_datetime, "%Y-%m-%d")
                )
            ).all()

        return {
            "date": [result.date for result in results],
            "count": [result.count for result in results],
        }


class EmptyMedia(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("media", action="append")

    def get(self, section_id: int):
        with Session(engine) as session:
            results = (
                session.query(
                    model.EmptyMedia.section,
                    func.date_format(
                        model.EmptyMedia.medium_datetime, "%Y-%m-%d %H:%i:%S"
                    ).label("medium_datetime"),
                    model.EmptyMedia.path,
                )
                .filter(
                    and_(
                        model.EmptyMedia.section == section_id,
                        model.EmptyMedia.checked == False,
                    )
                )
                .all()
            )
        return [result._asdict() for result in results]

    def post(self, section_id: int):
        arg = self.parser.parse_args()

        media = []
        for medium in arg.media:
            m = ast.literal_eval(medium)
            media.append(
                model.EmptyMedia(
                    section=section_id,
                    medium_datetime=m["medium_datetime"],
                    path=m["path"],
                )
            )

        with Session(engine) as session:
            session.add_all(media)
            session.commit()


class EmptyCheckPerchMount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("media", action="append")

    def get(self, perch_mount_id: int, limit: int):
        with Session(engine) as session:
            results = (
                session.query(
                    model.EmptyMedia.empty_medium_id,
                    model.EmptyMedia.section,
                    func.date_format(
                        model.EmptyMedia.medium_datetime, "%Y-%m-%d %H:%i:%S"
                    ).label("medium_datetime"),
                    model.EmptyMedia.path,
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.EmptyMedia.section,
                    isouter=True,
                )
                .filter(
                    and_(
                        model.Sections.perch_mount == perch_mount_id,
                        model.EmptyMedia.checked == False,
                    )
                )
                .order_by(model.EmptyMedia.medium_datetime)
                .limit(limit)
                .all()
            )
        return [result._asdict() for result in results]

    def put(self):
        arg = self.parser.parse_args()

        if not arg.media:
            return {"message": None}

        media = []
        medium_ids = []

        for medium in arg.media:
            m = ast.literal_eval(medium)
            new_medium = model.DetectedMedia(
                detected_medium_id=m["empty_medium_id"],
                section=m["section"],
                medium_datetime=m["medium_datetime"],
                path=m["path"],
                empty_checker=m["empty_checker"],
            )
            media.append(new_medium)
            medium_ids.append(m["empty_medium_id"])

        if self._is_media_checked(medium_ids):
            return {"message": "there is medium has been checked."}

        with Session(engine) as session:
            session.query(model.EmptyMedia).filter(
                model.EmptyMedia.empty_medium_id.in_(medium_ids)
            ).update({"checked": True})
            session.add_all(media)
            session.commit()

        return {"message": None}

    def delete(self):
        arg = self.parser.parse_args()
        medium_ids = []
        paths = []
        if not arg.media:
            return {"message": None}

        for medium in arg.media:
            m = ast.literal_eval(medium)
            paths.append(m["path"])
            medium_ids.append(m["empty_medium_id"])

        if self._is_media_checked(medium_ids):
            return {"message": "There is medium has been checked."}

        with Session(engine) as session:
            session.query(model.EmptyMedia).filter(
                model.EmptyMedia.empty_medium_id.in_(medium_ids)
            ).update({"checked": True})
            session.commit()

        for path in paths:
            file.move_to_empty(path)

        return {"message": None}

    def _is_media_checked(self, medium_ids: list[str]) -> bool:
        with Session(engine) as session:
            results = (
                session.query(model.EmptyMedia.checked)
                .filter(model.EmptyMedia.empty_medium_id.in_(medium_ids))
                .all()
            )
        return any(result.checked for result in results)


class ReviewPerchMount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("media", action="append")

    def get(self, perch_mount_id: int, limit: int):
        media = (
            select(
                model.DetectedMedia.detected_medium_id,
                model.DetectedMedia.section,
                func.date_format(
                    model.DetectedMedia.medium_datetime, "%Y-%m-%d %H:%i:%S"
                ).label("medium_datetime"),
                model.DetectedMedia.path,
                model.DetectedMedia.empty_checker,
            )
            .join(
                model.Sections,
                model.Sections.section_id == model.DetectedMedia.section,
                isouter=True,
            )
            .filter(
                and_(
                    model.Sections.perch_mount == perch_mount_id,
                    model.DetectedMedia.reviewed == False,
                )
            )
            .order_by(model.DetectedMedia.medium_datetime)
            .limit(limit)
            .subquery()
        )
        with Session(engine) as session:
            results = (
                session.query(
                    model.DetectedIndividuals.taxon_order_by_ai,
                    model.DetectedIndividuals.xmin,
                    model.DetectedIndividuals.xmax,
                    model.DetectedIndividuals.ymin,
                    model.DetectedIndividuals.ymax,
                    model.Species.chinese_common_name,
                    media.c.detected_medium_id,
                    media.c.section,
                    media.c.medium_datetime,
                    media.c.path,
                    media.c.empty_checker,
                )
                .join(
                    model.DetectedIndividuals,
                    media.c.detected_medium_id == model.DetectedIndividuals.medium,
                    isouter=True,
                )
                .join(
                    model.Species,
                    model.Species.taxon_order
                    == model.DetectedIndividuals.taxon_order_by_ai,
                    isouter=True,
                )
                .order_by()
                .all()
            )

        media_results = []
        last_id = ""
        for result in results:
            if result.detected_medium_id != last_id:
                medium = {
                    "detected_medium_id": result.detected_medium_id,
                    "section": result.section,
                    "medium_datetime": result.medium_datetime,
                    "path": result.path,
                    "empty_checker": result.empty_checker,
                    "individuals": [],
                }
                media_results.append(medium)
                last_id = result.detected_medium_id
            individual = {
                "taxon_order_by_ai": result.taxon_order_by_ai,
                "common_name_by_ai": result.chinese_common_name,
                "xmin": result.xmin,
                "xmax": result.xmax,
                "ymin": result.ymin,
                "ymax": result.ymax,
            }
            media_results[-1]["individuals"].append(individual)

        return media_results

    def put(self):
        arg = self.parser.parse_args()

        if not arg.media:
            return {"message": None}

        media = []
        medium_ids = []
        individuals = []

        # print(arg.media)

        for medium in arg.media:
            m = ast.literal_eval(medium)
            medium_ids.append(m["detected_medium_id"])
            new_medium = model.Media(
                medium_id=m["detected_medium_id"],
                section=m["section"],
                medium_datetime=m["medium_datetime"],
                path=m["path"],
                empty_checker=m["empty_checker"],
                reviewer=m["reviewer"],
                event=m["event"],
                # featured=m["featured"],
                featured_by=m["featured_by"],
                featured_title=m["featured_title"],
                featured_behavior=m["featured_behavior"],
            )
            media.append(new_medium)

            for individual in m["individuals"]:
                new_individual = model.Individuals(
                    medium=m["detected_medium_id"],
                    taxon_order_by_ai=individual["taxon_order_by_ai"],
                    taxon_order_by_human=individual["taxon_order_by_human"],
                    prey=individual["prey"],
                    tagged=individual["tagged"],
                    ring_number=individual["ring_number"],
                    xmin=individual["xmin"],
                    xmax=individual["xmax"],
                    ymin=individual["ymin"],
                    ymax=individual["ymax"],
                )
                individuals.append(new_individual)

        if self._is_media_checked(medium_ids):
            return {"message": "There is medium has been checked."}

        with Session(engine) as session:
            session.add_all(media)
            session.query(model.DetectedMedia).filter(
                model.DetectedMedia.detected_medium_id.in_(medium_ids)
            ).update({"reviewed": True})
            session.commit()

        with Session(engine) as session:
            session.add_all(individuals)
            session.commit()

        return {"message": None}

    def delete(self):
        arg = self.parser.parse_args()

        if not arg.media:
            return {"message": None}

        medium_ids = []
        paths = []

        for medium in arg.media:
            m = ast.literal_eval(medium)
            medium_ids.append(m["detected_medium_id"])
            paths.append(m["path"])

        if self._is_media_checked(medium_ids):
            return {"message": "There is medium has been checked."}

        with Session(engine) as session:
            session.query(model.DetectedMedia).filter(
                model.DetectedMedia.detected_medium_id.in_(medium_ids)
            ).update({"reviewed": True})
            session.commit()

        for path in paths:
            file.move_to_empty(path)

        return {"message": None}

    def _is_media_checked(self, medium_ids: list[str]) -> bool:
        with Session(engine) as session:
            results = (
                session.query(model.DetectedMedia.reviewed)
                .filter(model.DetectedMedia.detected_medium_id.in_(medium_ids))
                .all()
            )
        return any(result.reviewed for result in results)


class EmptyCheckSection(Resource):
    def get(self, section_id: int, limit: int):
        with Session(engine) as session:
            results = (
                session.query(
                    model.EmptyMedia.empty_medium_id,
                    model.EmptyMedia.section,
                    func.date_format(
                        model.EmptyMedia.medium_datetime, "%Y-%m-%d %H:%i:%S"
                    ).label("medium_datetime"),
                    model.EmptyMedia.path,
                )
                .join(
                    model.Sections,
                    model.Sections.section_id == model.EmptyMedia.section,
                    isouter=True,
                )
                .filter(
                    and_(
                        model.Sections.section_id == section_id,
                        model.EmptyMedia.checked == False,
                    )
                )
                .order_by(model.EmptyMedia.medium_datetime)
                .limit(limit)
                .all()
            )
        return [result._asdict() for result in results]


class ReviewPerchSection(Resource):
    def get(self, section_id: int, limit: int):
        media = (
            select(
                model.DetectedMedia.detected_medium_id,
                model.DetectedMedia.section,
                func.date_format(
                    model.DetectedMedia.medium_datetime, "%Y-%m-%d %H:%i:%S"
                ).label("medium_datetime"),
                model.DetectedMedia.path,
                model.DetectedMedia.empty_checker,
            )
            .join(
                model.Sections,
                model.Sections.section_id == model.DetectedMedia.section,
                isouter=True,
            )
            .filter(
                and_(
                    model.Sections.section_id == section_id,
                    model.DetectedMedia.reviewed == False,
                )
            )
            .order_by(model.DetectedMedia.medium_datetime)
            .limit(limit)
            .subquery()
        )
        with Session(engine) as session:
            results = (
                session.query(
                    model.DetectedIndividuals.taxon_order_by_ai,
                    model.DetectedIndividuals.xmin,
                    model.DetectedIndividuals.xmax,
                    model.DetectedIndividuals.ymin,
                    model.DetectedIndividuals.ymax,
                    model.Species.chinese_common_name,
                    media.c.detected_medium_id,
                    media.c.section,
                    media.c.medium_datetime,
                    media.c.path,
                    media.c.empty_checker,
                )
                .join(
                    model.DetectedIndividuals,
                    media.c.detected_medium_id == model.DetectedIndividuals.medium,
                    isouter=True,
                )
                .join(
                    model.Species,
                    model.Species.taxon_order
                    == model.DetectedIndividuals.taxon_order_by_ai,
                    isouter=True,
                )
                .order_by()
                .all()
            )
        media_results = []
        last_id = ""
        for result in results:
            if result.detected_medium_id != last_id:
                medium = {
                    "detected_medium_id": result.detected_medium_id,
                    "section": result.section,
                    "medium_datetime": result.medium_datetime,
                    "path": result.path,
                    "empty_checker": result.empty_checker,
                    "individuals": [],
                }
                media_results.append(medium)
                last_id = result.detected_medium_id
            individual = {
                "taxon_order_by_ai": result.taxon_order_by_ai,
                "common_name_by_ai": result.chinese_common_name,
                "xmin": result.xmin,
                "xmax": result.xmax,
                "ymin": result.ymin,
                "ymax": result.ymax,
            }
            media_results[-1]["individuals"].append(individual)

        return media_results
