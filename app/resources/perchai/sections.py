import flask_restx
import flask_jwt_extended
import uuid

from app.services import perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.utils as resource_utils
from app.error_handler import errors
from app import model
from app.auth import admin_authorized


class Sections(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Sections.get)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.SectionFilter(**parsed_args)
        sections = perchai_service.sections.get_sections_by_filter(filter)
        return [section.to_dict() for section in sections]

    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.Sections.post)
    def post(self, parsed_args):
        new_section = perchai_service.sections.add_section(**parsed_args)
        return new_section.to_dict()


class Section(flask_restx.Resource):
    def get(self, section_id: uuid.UUID):
        section = perchai_service.sections.get_section_by_id(section_id)

        if section is None:
            raise errors.ResourceNotFoundError(model.Sections.__name__)

        return section.to_dict()

    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    @resource_utils.parse_args(parsers.Section.patch)
    def patch(self, section_id: uuid.UUID, parsed_args):
        perchai_service.sections.update_section(section_id, parsed_args)
        section = perchai_service.sections.get_section_by_id(section_id)
        return section.to_dict()

    @flask_jwt_extended.jwt_required()
    def delete(self, section_id: uuid.UUID):
        perchai_service.sections.delete_section(section_id)


class SectionSwappers(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    @resource_utils.parse_args(parsers.SectionSwappers.put)
    def put(self, section_id: uuid.UUID, parsed_args):
        perchai_service.sections.update_section_swappers(
            section_id, parsed_args["swapper_ids"]
        )
        section = perchai_service.sections.get_section_by_id(section_id)
        return section.to_dict()


class SectionTime(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    @resource_utils.parse_args(parsers.SectionTime.patch)
    def patch(self, section_id: uuid.UUID, parsed_args):
        perchai_service.sections.shift_section_times(
            section_id, parsed_args["start_time"]
        )
        section = perchai_service.sections.get_section_by_id(section_id)
        return section.to_dict()
