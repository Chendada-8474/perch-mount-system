import flask_restx
import flask_jwt_extended
import uuid

from app.services import perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.utils as resource_utils
from app.auth import admin_authorized
from app.error_handler import errors
from app import model


class Media(flask_restx.Resource):
    @resource_utils.parse_args(parsers.Media.get)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.MediaFilter(**parsed_args)
        media = perchai_service.media.get_media_by_filter(filter)
        return [medium.to_dict() for medium in media]


class Medium(flask_restx.Resource):
    def get(self, medium_id: uuid.UUID):
        medium = perchai_service.media.get_medium_by_id(medium_id)

        if medium is None:
            raise errors.ResourceNotFoundError(model.Media.__name__)

        return medium.to_dict()

    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.Medium.patch)
    def patch(self, medium_id: uuid.UUID, parsed_args):
        medium = perchai_service.media.get_medium_by_id(medium_id)
        if medium.status != model.enums.MediaStatus.REVIEWED:
            raise errors.MediaStatusError()
        perchai_service.media.update_medium_by_id(medium_id, parsed_args)


class MediumStatus(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    @resource_utils.parse_args(parsers.MediumStatus.patch)
    def patch(self, medium_id: uuid.UUID, parsed_args):
        medium = perchai_service.media.get_medium_by_id(medium_id)
        if (
            parsed_args["status"] != model.enums.MediaStatus.UNREVIEWED.value
            or medium.status != model.enums.MediaStatus.REVIEWED
        ):
            raise errors.MediaStatusRollbackError()

        perchai_service.media_operation.rollback_reviewed_medium_status(medium_id)
        medium = perchai_service.media.get_medium_by_id(medium_id)
        return medium.to_dict()


class MediumFeature(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.MediumFeature.patch)
    def patch(self, medium_id: uuid.UUID, parsed_args: dict):
        perchai_service.media.update_media_feature(medium_id, parsed_args)
        medium = perchai_service.media.get_medium_by_id(medium_id)
        return medium.to_dict()


class UploadedMedia(flask_restx.Resource):
    # @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.UploadedMedia.post)
    def post(self, section_id: uuid.UUID, parsed_args):
        section = perchai_service.sections.get_section_by_id(section_id)
        if section.start_time:
            raise errors.SectionAlreadyGotDataError()

        perchai_service.media_operation.add_uploaded_media(section_id, parsed_args)


class DetectedMedia(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.DetectedMedia.post)
    def post(self, parsed_args):
        perchai_service.media_operation.add_detected_media(parsed_args)


class CheckedMedia(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.CheckedMedia.post)
    def post(self, parsed_args):
        perchai_service.media_operation.add_checked_media(parsed_args)


class ReviewedMedia(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.ReviewedMedia.post)
    def post(self, parsed_args):
        perchai_service.media_operation.add_reviewed_media(parsed_args)
