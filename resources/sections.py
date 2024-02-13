import datetime
import flask
import flask_restful
import flask_restful.reqparse

import resources
import resources.utils
import service.sections as ServiceSections
import service.members as ServiceMembers
import service.cameras as ServiceCameras
import service.mount_types as ServiceMountTypes


class Sections(resources.PerchMountResource):
    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        sections = ServiceSections.get_sections(**args)
        sections = [row.to_json() for row in sections]

        section_indice = resources.utils.get_nodup_values(sections, "section_id")
        operator_map = self._get_operator_map(section_indice)
        self._find_operator_to_sections(sections, operator_map)

        members = ServiceMembers.get_operators_by_section_indice(section_indice)
        cameras = ServiceCameras.get_cameras()
        mount_types = ServiceMountTypes.get_mount_types()

        members = [row.to_json() for row in members]
        cameras = [row.to_json() for row in cameras]
        mount_types = [row.to_json() for row in mount_types]

        return {
            "sections": sections,
            "members": resources.utils.field_as_key(members, "member_id"),
            "cameras": resources.utils.field_as_key(cameras, "camera_id"),
            "mount_types": resources.utils.field_as_key(mount_types, "mount_type_id"),
        }

    def _get_operator_map(self, section_indice: list[int]) -> dict:
        operators = ServiceSections.get_section_operators(section_indice)
        operator_map = resources.utils.find_section_operator_map(operators)
        return operator_map

    def _find_operator_to_sections(self, sections: list[dict], operator_map: dict):
        for section in sections:
            section["operators"] = operator_map[section["section_id"]]


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
            "members": resources.utils.field_as_key(members, "member_id"),
        }

    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("perch_mount", type=int, required=True)
    post_parser.add_argument("mount_type", type=int, required=True)
    post_parser.add_argument("camera", type=int, required=True)
    post_parser.add_argument(
        "start_time", type=datetime.datetime.fromisoformat, required=True
    )
    post_parser.add_argument(
        "end_time", type=datetime.datetime.fromisoformat, required=True
    )
    post_parser.add_argument(
        "check_date", type=datetime.date.fromisoformat, required=True
    )
    post_parser.add_argument("valid", type=bool, required=True)
    post_parser.add_argument(
        "operators", type=list[int], required=True, location="json"
    )
    post_parser.add_argument("note", type=str)

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        section_id = ServiceSections.add_section(**args)
        return self.get(section_id)
