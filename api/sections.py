from datetime import datetime, date
import flask
import flask_restful
from flask_restful import reqparse

from api import utils
import service.sections as ServiceSections
import service.members as ServiceMembers
import service.cameras as ServiceCameras
import service.mount_types as ServiceMountTypes


class Sections(flask_restful.Resource):
    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        results = ServiceSections.get_sections(**args)
        results = [row.to_json() for row in results]

        section_indice = utils.get_nodup_values(results, "section_id")

        members = ServiceMembers.get_operators_by_section_indice(section_indice)
        cameras = ServiceCameras.get_cameras()
        mount_types = ServiceMountTypes.get_mount_types()

        members = [row.to_json() for row in members]
        cameras = [row.to_json() for row in cameras]
        mount_types = [row.to_json() for row in mount_types]

        return {
            "sections": results,
            "members": utils.field_as_key(members, "member_id"),
            "cameras": utils.field_as_key(cameras, "camera_id"),
            "mount_types": utils.field_as_key(mount_types, "mount_type_id"),
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


class Section(flask_restful.Resource):
    def get(self, section_id: int):
        section = ServiceSections.get_section_by_id(section_id)
        members = ServiceMembers.get_operators_by_section_indice([section.section_id])
        camera = ServiceCameras.get_camera_by_id(section.camera)
        mount_type = ServiceMountTypes.get_mount_type_by_id(section.mount_type)

        members = [row.to_json() for row in members]

        return {
            "section": section.to_json(),
            "camera": camera.to_json(),
            "mount_type": mount_type.to_json(),
            "members": utils.field_as_key(members, "member_id"),
        }

    post_parser = reqparse.RequestParser()
    post_parser.add_argument("perch_mount", type=int, required=True)
    post_parser.add_argument("mount_type", type=int, required=True)
    post_parser.add_argument("camera", type=int, required=True)
    post_parser.add_argument("start_time", type=datetime.fromisoformat, required=True)
    post_parser.add_argument("end_time", type=datetime.fromisoformat, required=True)
    post_parser.add_argument("check_date", type=date.fromisoformat, required=True)
    post_parser.add_argument("valid", type=bool, required=True)
    post_parser.add_argument(
        "operators", type=list[int], required=True, location="json"
    )
    post_parser.add_argument("note", type=str)

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        section_id = ServiceSections.add_section(**args)
        return self.get(section_id)
