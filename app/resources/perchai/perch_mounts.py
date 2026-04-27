import flask_restx
import flask_jwt_extended
import uuid

from app.services import perchai as perchai_service
from app.resources.perchai import parsers
import app.resources.utils as resource_utils
from app.error_handler import errors
from app import model
from app.auth import admin_authorized
import app.resources.perchai.marshals.perch_mounts_pending_counts as pending_counts_marshals


class PerchMounts(flask_restx.Resource):

    @resource_utils.parse_args(parsers.PerchMounts.get)
    def get(self, parsed_args):
        filter = perchai_service.utils.query_filter.PerchMountFilter(**parsed_args)
        perch_mounts = perchai_service.perch_mounts.get_perch_mounts_by_filter(filter)
        return [perch_mount.to_dict() for perch_mount in perch_mounts]

    @flask_jwt_extended.jwt_required()
    @resource_utils.parse_args(parsers.PerchMounts.post)
    def post(self, parsed_args):
        new_perch_mount_id = perchai_service.perch_mounts.add_perch_mount(**parsed_args)
        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(
            new_perch_mount_id
        )
        return perch_mount.to_dict()


class PerchMount(flask_restx.Resource):
    def get(self, perch_mount_id: uuid.UUID):
        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)

        if perch_mount is None:
            raise errors.ResourceNotFoundError(model.PerchMounts.__name__)

        return perch_mount.to_dict()

    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    @resource_utils.parse_args(parsers.PerchMount.patch)
    def patch(self, perch_mount_id: uuid.UUID, parsed_args):
        perchai_service.perch_mounts.update_perch_mount(perch_mount_id, parsed_args)
        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        return perch_mount.to_dict()


class PerchMountClaimBy(flask_restx.Resource):
    def get(self, perch_mount_id: uuid.UUID):
        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        if perch_mount.claim_by_id:
            member = perchai_service.members.get_member_by_id(perch_mount.claim_by_id)
            return member.to_dict()

    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    @resource_utils.parse_args(parsers.PerchMountClaimBy.post)
    def post(self, perch_mount_id: uuid.UUID, parsed_args):
        perchai_service.perch_mounts.update_perch_mount(perch_mount_id, **parsed_args)

        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)

        return perch_mount.to_dict()

    def delete(self, perch_mount_id: uuid.UUID):
        perchai_service.perch_mounts.update_perch_mount(
            perch_mount_id,
            {"claim_by_id": None},
        )

        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)

        return perch_mount.to_dict()


class PerchMountClaimByMe(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self, perch_mount_id: uuid.UUID):
        claim_by_id = flask_jwt_extended.get_jwt_identity()
        perchai_service.perch_mounts.update_perch_mount(
            perch_mount_id,
            {"claim_by_id": claim_by_id},
        )

        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        return perch_mount.to_dict()

    @flask_jwt_extended.jwt_required()
    def delete(self, perch_mount_id: uuid.UUID):
        claim_by_id = flask_jwt_extended.get_jwt_identity()
        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)

        if str(perch_mount.claim_by_id) != claim_by_id:
            raise errors.Unauthorized("Perch Mount is not claimed by you")

        perchai_service.perch_mounts.update_perch_mount(
            perch_mount_id,
            {"claim_by_id": None},
        )

        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        return perch_mount.to_dict()


class PerchMountActivation(flask_restx.Resource):
    def get(self, perch_mount_id: uuid.UUID):
        perch_mount = perchai_service.perch_mounts.is_perch_mount_activated(
            perch_mount_id
        )
        if perch_mount is None:
            raise errors.ResourceNotFoundError(model.PerchMounts.__name__)
        return not perch_mount.terminated

    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    def post(self, perch_mount_id: uuid.UUID):
        perchai_service.perch_mounts.activate_perch_mount(perch_mount_id)
        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        return perch_mount.to_dict()

    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    def delete(self, perch_mount_id: uuid.UUID):
        perchai_service.perch_mounts.terminate_perch_mount(perch_mount_id)
        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        return perch_mount.to_dict()


class PerchMountPriority(flask_restx.Resource):
    def post(self, perch_mount_id: uuid.UUID):
        perchai_service.perch_mounts.update_perch_mount(
            perch_mount_id, {"is_priority": True}
        )

        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        return perch_mount.to_dict()

    def delete(self, perch_mount_id):
        perchai_service.perch_mounts.update_perch_mount(
            perch_mount_id, {"is_priority": False}
        )

        perch_mount = perchai_service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        return perch_mount.to_dict()


class PerchMountsPendingCounts(flask_restx.Resource):
    @flask_restx.marshal_with(pending_counts_marshals.COUNTS_MODEL)
    def get(self):
        counts = perchai_service.perch_mounts.get_perch_mounts_pending_counts()
        return [count._asdict() for count in counts]


class PerchMountPendingCounts(flask_restx.Resource):
    @flask_restx.marshal_with(pending_counts_marshals.COUNTS_MODEL)
    def get(self, perch_mount_id: uuid.UUID):
        count = perchai_service.perch_mounts.get_perch_mount_pending_counts_by_id(
            perch_mount_id
        )
        return count._asdict()


class PerchMountMonthlyCounts(flask_restx.Resource):
    def get(sef, perch_mount_id: uuid.UUID):
        return perchai_service.perch_mounts.get_perch_mount_monthly_counts(
            perch_mount_id
        )
