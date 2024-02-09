import flask_restful
from resources import *

api = flask_restful.Api()

api.add_resource(perch_mounts.PerchMounts, "/perch_mounts")
api.add_resource(
    perch_mounts.PerchMount, "/perch_mounts/<int:perch_mount_id>", "/perch_mounts"
)
api.add_resource(sections.Sections, "/sections")
api.add_resource(sections.Section, "/sections/<int:section_id>", "/sections")
api.add_resource(empty_media.EmptyMedia, "/empty_media")
api.add_resource(detected_media.DetectedMedia, "/detected_media")
