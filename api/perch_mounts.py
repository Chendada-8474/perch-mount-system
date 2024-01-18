from flask import request
from flask_restful import Resource, reqparse
from src.model import PerchMounts
from api.utils import field_as_key, get_nodup_values
import service.perch_mounts as ServicePerchMounts
import service.habitats as ServiceHabitats
import service.members as ServiceMembers
import service.projects as ServiceProjects


class PerchMounts(Resource):
    def get(self):
        args = dict(request.args)
        args = self._correct_types(args)
        results = ServicePerchMounts.get_perch_mounts(**args)
        results = [row.to_json() for row in results]
        project_indice = get_nodup_values(results, "project")
        habitat_indice = get_nodup_values(results, "habitat")
        claimer_indice = get_nodup_values(results, "claim_by")

        projects = ServiceProjects.get_projects_by_indice(project_indice)
        habitats = ServiceHabitats.get_habitats_by_indice(habitat_indice)
        members = ServiceMembers.get_member_by_indice(claimer_indice)

        projects = [row.to_json() for row in projects]
        habitats = [row.to_json() for row in habitats]
        members = [row.to_json() for row in members]

        return {
            "perch_mounts": results,
            "projects": field_as_key(projects, "project_id"),
            "habitats": field_as_key(habitats, "habitat_id"),
            "members": field_as_key(members, "member_id"),
        }

    def _correct_types(self, args: dict) -> dict:
        if "project" in args:
            args["project"] == int(args["project"])
        if "habitat" in args:
            args["habitat"] == int(args["habitat"])
        if "terminated" in args:
            args["terminated"] = args["terminated"].lower() == "true"
        if "claim_by" in args:
            args["claim_by"] == int(args["claim_by"])
        return args


class PerchMount(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument("perch_mount_name", type=str, required=True)
    post_parser.add_argument("latitude", type=float, required=True)
    post_parser.add_argument("longitude", type=float, required=True)
    post_parser.add_argument("habitat", type=int, required=True)
    post_parser.add_argument("project", type=int, required=True)
    post_parser.add_argument("layer", type=int)

    patch_parser = reqparse.RequestParser()
    patch_parser.add_argument("perch_mount_name", type=str)
    patch_parser.add_argument("latitude", type=float)
    patch_parser.add_argument("longitude", type=float)
    patch_parser.add_argument("habitat", type=int)
    patch_parser.add_argument("project", type=int)
    patch_parser.add_argument("layer", type=int)
    patch_parser.add_argument("terminated", type=bool)
    patch_parser.add_argument("is_priority", type=bool)

    def get(self, perch_mount_id: int):
        result = ServicePerchMounts.get_perch_mount_by_id(perch_mount_id)

        if not result:
            return

        project = ServiceProjects.get_project_by_id(result.project)
        habitat = ServiceHabitats.get_habitat_by_id(result.habitat)
        member = ServiceMembers.get_member_by_id(result.claim_by)
        return {
            "perch_mounts": result.to_json(),
            "projects": project.to_json(),
            "habitats": habitat.to_json(),
            "members": member.to_json() if member else {},
        }

    def post(self):
        args = self.post_parser.parse_args()
        perch_mount = ServicePerchMounts.add_perch_mount(**args)
        return perch_mount.to_json()

    def patch(self):
        args = self.patch_parser.parse_args()
        return
