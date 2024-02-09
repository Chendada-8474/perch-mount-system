import flask
import flask_restful.reqparse

import api
import service.behaviors as ServiceBehaviors
import service.cameras as ServiceCameras
import service.events as ServiceEvents
import service.habitats as ServiceHabitats
import service.layers as ServiceLayers
import service.mount_types as ServiceMountTypes
import service.projects as ServiceProjects
import service.positions as ServicePositions


class Behaviors(api.PerchMountResource):

    def get(self):
        behaviors = ServiceBehaviors.get_behaviors()
        return {"behaviors": [behavior.to_json() for behavior in behaviors]}


class Behavior(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("chinese_name", type=str, required=True)

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        behavior_id = ServiceBehaviors.add_behavior(args["chinese_name"])
        behavior = ServiceBehaviors.get_behavior_by_id(behavior_id)
        return behavior.to_json()


class Cameras(api.PerchMountResource):
    def get(self):
        cameras = ServiceCameras.get_cameras()
        return {"cameras": [camera.to_json() for camera in cameras]}


class Camera(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("model_name", type=str, required=True)

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        camera_id = ServiceCameras.add_camera(args["model_name"])
        camera = ServiceCameras.get_camera_by_id(camera_id)
        return camera.to_json()


class Events(api.PerchMountResource):
    def get(self):
        events = ServiceEvents.get_events()
        return {"events": [event.to_json() for event in events]}


class Event(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("chinese_name", type=str, required=True)
    post_parser.add_argument("english_name", type=str, required=True)

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        event_id = ServiceEvents.add_event(args["chinese_name"], args["english_name"])
        event = ServiceEvents.get_event_by_id(event_id)
        return event.to_json()


class Habitats(api.PerchMountResource):
    def get(self):
        habitats = ServiceHabitats.get_habitats()
        return {"habitats": [habitat.to_json() for habitat in habitats]}


class Habitat(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument(
        "chinese_name",
        type=str,
        required=True,
    )
    post_parser.add_argument(
        "english_name",
        type=str,
        required=True,
    )

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        habitat_id = ServiceHabitats.add_habitat(
            args["chinese_name"],
            args["english_name"],
        )
        habitat = ServiceHabitats.get_habitat_by_id(habitat_id)
        return habitat.to_json()


class Layers(api.PerchMountResource):
    def get(self):
        layers = ServiceLayers.get_layers()
        return {"layers": [layer.to_json() for layer in layers]}


class Layer(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("name", type=str, required=True)

    def get(self, layer_id: int):
        layer = ServiceLayers.get_layer_by_id(layer_id)
        return layer.to_json()

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        layer_id = ServiceLayers.add_layer(args["name"])
        layer = ServiceLayers.get_layer_by_id(layer_id)
        return layer.to_json()


class MountTypes(api.PerchMountResource):
    def get(self):
        mount_types = ServiceMountTypes.get_mount_types()
        return {"mount_types": [mount_type.to_json() for mount_type in mount_types]}


class MountType(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("name", type=str, required=True)

    def get(self, mount_type_id: int):
        mount_type = ServiceMountTypes.get_mount_type_by_id(mount_type_id)
        return mount_type.to_json()

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        layer_id = ServiceLayers.add_layer(args["name"])
        layer = ServiceLayers.get_layer_by_id(layer_id)
        return layer.to_json()


class Projects(api.PerchMountResource):
    def get(self):
        projects = ServiceProjects.get_projects()
        return {"projects": [project.to_json() for project in projects]}


class Project(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("name", type=str, required=True)

    def get(self, project_id: int):
        project = ServiceProjects.get_project_by_id(project_id)
        return project.to_json()

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        project_id = ServiceProjects.add_project(args["name"])
        project = ServiceProjects.get_project_by_id(project_id)
        return project.to_json()


class Positions(api.PerchMountResource):
    def get(self):
        positions = ServicePositions.get_positions()
        return {"positions": [position.to_json() for position in positions]}


class Position(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("name", type=str, required=True)

    def get(self, position_id: int):
        postion = ServicePositions.get_position_by_id(position_id)
        return postion.to_json()

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        position_id = ServicePositions.add_position(args["name"])
        position = ServicePositions.get_position_by_id(position_id)
        return position.to_json()
