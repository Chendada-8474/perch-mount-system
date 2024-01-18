from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
from api.utils import field_as_key, get_nodup_values
from src.model import PerchMounts, Sections, Cameras
import service.sections as ServiceSections
import service.members as ServiceMembers
import service.cameras as ServiceCameras
import service.mount_types as ServiceMountTypes


class Sections(Resource):
    def get(self):
        args = dict(request.args)
        args = self._correct_types(args)
        results = ServiceSections.get_sections(**args)
        results = [row.to_json() for row in results]

        section_indice = get_nodup_values(results, "section_id")

        members = ServiceMembers.get_operators_by_section_indice(section_indice)
        cameras = ServiceCameras.get_cameras()
        mount_types = ServiceMountTypes.get_mount_types()

        members = [row.to_json() for row in members]
        cameras = [row.to_json() for row in cameras]
        mount_types = [row.to_json() for row in mount_types]

        return {
            "sections": results,
            "members": field_as_key(members, "member_id"),
            "cameras": field_as_key(cameras, "camera_id"),
            "mount_types": field_as_key(mount_types, "mount_type_id"),
        }

    def _correct_types(self, args: dict) -> dict:
        if "perch_mount" in args:
            args["perch_mount"] == int(args["perch_mount"])
        if "check_date_from" in args:
            args["check_date_from"] = datetime.fromisoformat(args["check_date_from"])
        if "check_date_to" in args:
            args["check_date_to"] = datetime.fromisoformat(args["check_date_to"])
        if "operator" in args:
            args["operator"] == int(args["operator"])

        return args
