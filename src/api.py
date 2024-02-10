import flask_restful
from resources import perch_mounts
from resources import sections
from resources import empty_media
from resources import detected_media
from resources import media


# ROUTES = [
#     {
#         # perch_mounts
#         "route": "perch_mounts",
#         "resources": [perch_mounts.PerchMounts, perch_mounts.PerchMount],
#         "children": [
#             {
#                 "route": "<int:perch_mount_id>",
#                 "resource": perch_mounts.PerchMount,
#                 "children": [],
#             }
#         ],
#     },
#     {
#         # sections
#         "route": "sections",
#         "resources": [sections.Section, sections.Sections],
#         "children": [
#             {
#                 "route": "<int:section_id>",
#                 "resources": [sections.Section],
#                 "children": [],
#             }
#         ],
#     },
# ]


# class PerchMountApi(flask_restful.Api):
#     def add_resources(self, routes: list[dict], parent: str = "/"):
#         for route in routes:

#             for resource in route["resources"]:
#                 self.add_resource(resource, route["route"])

#             parent = f"{parent}{route}/"
#             self.add_resources(route["children"], parent=parent)


api = flask_restful.Api()

api.add_resource(perch_mounts.PerchMounts, "/perch_mounts")
api.add_resource(
    perch_mounts.PerchMount, "/perch_mounts/<int:perch_mount_id>", "/perch_mounts"
)
api.add_resource(sections.Sections, "/sections")
api.add_resource(sections.Section, "/sections/<int:section_id>", "/sections")
api.add_resource(empty_media.EmptyMedia, "/empty_media")
api.add_resource(detected_media.DetectedMedia, "/detected_media")
