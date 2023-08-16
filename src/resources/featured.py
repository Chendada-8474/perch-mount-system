import sys
from os.path import dirname
from flask_restful import Resource
from sqlalchemy.orm import Session
from sqlalchemy import and_, func


sys.path.append(dirname(dirname(dirname(__file__))))
from src.resources.db_engine import slave_engine, master_engine
import src.model as model
import configs.config as config


class FeaturedMedia(Resource):
    def get(
        self,
        page: int,
        perch_mount_name: int,
        behavior_id: int,
        chinese_common_name: str,
        member_id: int,
    ):
        conditions = [model.Media.featured_behavior.is_not(None)]

        if perch_mount_name != "$":
            conditions.append(model.PerchMounts.perch_mount_name == perch_mount_name)

        if chinese_common_name != "$":
            conditions.append(model.Species.chinese_common_name == chinese_common_name)

        if behavior_id:
            conditions.append(model.Media.featured_behavior == behavior_id)

        if member_id:
            conditions.append(model.Media.featured_by == member_id)

        columns = [
            model.Media.medium_id,
            model.Media.path,
            model.Media.featured_title,
            model.Behaviors.chinese_name.label("behavior"),
            model.Species.chinese_common_name.label("species"),
            model.PerchMounts.perch_mount_name,
            model.PerchMounts.perch_mount_id,
            model.Sections.section_id,
            model.Members.first_name.label("featured_by"),
        ]

        with Session(slave_engine) as session:
            results = self._query_all(session, columns, conditions)

        media = []
        medium_id = ""

        start = page * config.NUM_MEDIA_IN_PAGE
        end = start + config.NUM_MEDIA_IN_PAGE

        for result in results:
            if result.medium_id != medium_id:
                media.append(
                    {
                        "medium_id": result.medium_id,
                        "path": result.path,
                        "title": result.featured_title,
                        "behavior": result.behavior,
                        "perch_mount_name": result.perch_mount_name,
                        "perch_mount_id": result.perch_mount_id,
                        "section_id": result.section_id,
                        "featured_by": result.featured_by,
                        "species": [],
                    }
                )
                medium_id = result.medium_id
            media[-1]["species"].append(result.species)

        count = len(media)

        return {
            "count": count,
            "media": media[start:end],
        }

    def _query_all(self, session, columns: list, conditions: list):
        query = (
            session.query(*columns)
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
                model.Individuals,
                model.Individuals.medium == model.Media.medium_id,
                isouter=True,
            )
            .join(
                model.Species,
                model.Species.taxon_order == model.Individuals.taxon_order_by_human,
                isouter=True,
            )
            .join(
                model.Behaviors,
                model.Behaviors.behavior_id == model.Media.featured_behavior,
                isouter=True,
            )
            .join(
                model.Members,
                model.Media.featured_by == model.Members.member_id,
                isouter=True,
            )
            .filter(and_(*conditions))
            .order_by(model.Media.medium_datetime)
            .all()
        )
        return query


class FeaturedMedium(Resource):
    def delete(self, medium_id: str):
        with Session(master_engine) as session:
            session.query(model.Media).filter(
                model.Media.medium_id == medium_id
            ).update(
                {
                    "featured_behavior": None,
                    "featured_by": None,
                    "featured_title": None,
                }
            )
            session.commit()
