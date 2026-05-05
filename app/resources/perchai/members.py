import flask_restx
import flask_jwt_extended
import uuid

from app.resources.perchai import parsers
import app.services.perchai as perchai_service
import app.resources.perchai.utils as perchai_utils
import app.resources.utils as resource_utils
from app.error_handler import errors
from app import model
from app.auth import admin_authorized


class Members(flask_restx.Resource):
    def get(self):
        members = perchai_service.members.get_members()
        return [member.to_dict() for member in members]


class Member(flask_restx.Resource):
    def get(self, member_id: uuid.UUID):
        member = perchai_service.members.get_member_by_id(member_id)

        if member is None:
            raise errors.ResourceNotFoundError(model.Members.__name__)

        return member.to_dict()

    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    @resource_utils.parse_args(parsers.Member.patch)
    def patch(self, member_id: uuid.UUID, parsed_args: dict):
        perchai_service.members.update_member_by_id(member_id, parsed_args)
        member = perchai_service.members.get_member_by_id(member_id)
        return member.to_dict()


class MemberBlock(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @admin_authorized.super_admin_required()
    def post(self, member_id: uuid.UUID):
        perchai_service.members.block_member(member_id)
        member = perchai_service.members.get_member_by_id(member_id)
        return member.to_dict()

    @flask_jwt_extended.jwt_required()
    @admin_authorized.super_admin_required()
    def delete(self, member_id: uuid.UUID):
        member = perchai_service.members.get_member_by_id(member_id)
        perchai_service.members.unblock_member(member_id)
        return member.to_dict()


class MemberActivation(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @admin_authorized.super_admin_required()
    def post(self, member_id: uuid.UUID):
        member = perchai_service.members.get_member_by_id(member_id)
        perchai_service.members.activate_member(member_id)
        return member.to_dict()

    @flask_jwt_extended.jwt_required()
    @admin_authorized.super_admin_required()
    def delete(self, member_id: uuid.UUID):
        perchai_service.members.deactivate_member(member_id)
        member = perchai_service.members.get_member_by_id(member_id)
        return member.to_dict()


class MemberAdmin(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @admin_authorized.admin_required()
    def post(self, member_id: uuid.UUID):
        perchai_service.members.grant_admin_privileges(member_id)
        member = perchai_service.members.get_member_by_id(member_id)
        return member.to_dict()

    @flask_jwt_extended.jwt_required()
    @admin_authorized.super_admin_required()
    def delete(self, member_id: uuid.UUID):
        perchai_service.members.ungrant_admin_privileges(member_id)
        member = perchai_service.members.get_member_by_id(member_id)
        return member.to_dict()


class MemberSuperAdmin(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @admin_authorized.super_admin_required()
    def post(self, member_id: uuid.UUID):
        perchai_service.members.ungrant_admin_privileges(member_id)
        member = perchai_service.members.get_member_by_id(member_id)
        return member.to_dict()


class MemberClaimedPerchMouns(flask_restx.Resource):
    def get(self, member_id: uuid.UUID):
        filter = perchai_service.utils.query_filter.PerchMountFilter(
            claim_by_ids=[member_id]
        )
        perch_mounts = perchai_service.perch_mounts.get_perch_mounts_by_filter(filter)
        return [perch_mount.to_dict() for perch_mount in perch_mounts]
