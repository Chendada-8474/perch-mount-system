import flask
import flask_restful
import flask_restful.reqparse

import cache
import cache.key
import config
import service.perch_mounts
import service.habitats
import service.members
import service.projects
import resources
import resources.utils


TIMEOUT = config.get_data_cache_timeout()


class PerchMounts(resources.PerchMountResource):
    @cache.cache.cached(timeout=TIMEOUT, make_cache_key=cache.key.key_generate)
    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)

        results = service.perch_mounts.get_perch_mounts(**args)
        results = [row.to_json() for row in results]
        project_indice = resources.utils.get_nodup_values(results, "project")
        habitat_indice = resources.utils.get_nodup_values(results, "habitat")
        claimer_indice = resources.utils.get_nodup_values(results, "claim_by")

        projects = service.projects.get_projects_by_indice(project_indice)
        habitats = service.habitats.get_habitats_by_indice(habitat_indice)
        members = service.members.get_member_by_indice(claimer_indice)

        projects = [row.to_json() for row in projects]
        habitats = [row.to_json() for row in habitats]
        members = [row.to_json() for row in members]

        return {
            "perch_mounts": results,
            "projects": resources.utils.field_as_key(projects, "project_id"),
            "habitats": resources.utils.field_as_key(habitats, "habitat_id"),
            "members": resources.utils.field_as_key(members, "member_id"),
        }


class PerchMount(flask_restful.Resource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("perch_mount_name", type=str, required=True)
    post_parser.add_argument("latitude", type=float, required=True)
    post_parser.add_argument("longitude", type=float, required=True)
    post_parser.add_argument("habitat", type=int, required=True)
    post_parser.add_argument("project", type=int, required=True)
    post_parser.add_argument("layer", type=int)

    patch_parser = flask_restful.reqparse.RequestParser()
    patch_parser.add_argument("perch_mount_name", type=str)
    patch_parser.add_argument("latitude", type=float)
    patch_parser.add_argument("longitude", type=float)
    patch_parser.add_argument("habitat", type=int)
    patch_parser.add_argument("project", type=int)
    patch_parser.add_argument("layer", type=int)
    patch_parser.add_argument("terminated", type=bool)
    patch_parser.add_argument("is_priority", type=bool)

    @cache.cache.cached(timeout=TIMEOUT, make_cache_key=cache.key.key_generate)
    def get(self, perch_mount_id: int):
        result = service.perch_mounts.get_perch_mount_by_id(perch_mount_id)

        if not result:
            return

        project = service.projects.get_project_by_id(result.project)
        habitat = service.habitats.get_habitat_by_id(result.habitat)
        member = service.members.get_member_by_id(result.claim_by)
        return {
            "perch_mounts": result.to_json(),
            "projects": project.to_json(),
            "habitats": habitat.to_json(),
            "members": member.to_json() if member else {},
        }

    def post(self):
        args = self.post_parser.parse_args()
        perch_mount_id = service.perch_mounts.add_perch_mount(**args)
        perch_mount = service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        cache.key.evict_same_path_keys()
        return perch_mount.to_json()

    def patch(self, perch_mount_id: int):
        self.patch_parser.parse_args(strict=True)
        args = flask.request.get_json()
        service.perch_mounts.update_perch_mount(perch_mount_id, args)
        perch_mount = service.perch_mounts.get_perch_mount_by_id(perch_mount_id)
        cache.key.evict_same_path_keys()
        return perch_mount.to_json()
