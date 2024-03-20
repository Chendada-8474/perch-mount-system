import flask_restful.reqparse
import flask_jwt_extended

import cache
import cache.key
import resources
import service.behaviors
import service.cameras
import service.events
import service.habitats
import service.layers
import service.mount_types
import service.projects
import service.positions


class Behaviors(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        behaviors = service.behaviors.get_behaviors()
        return {"behaviors": [behavior.to_json() for behavior in behaviors]}


class Behavior(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("chinese_name", type=str, required=True)

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        behavior_id = service.behaviors.add_behavior(args["chinese_name"])
        behavior = service.behaviors.get_behavior_by_id(behavior_id)
        cache.key.evict_same_path_keys()
        return behavior.to_json()


class Cameras(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        cameras = service.cameras.get_cameras()
        return {"cameras": [camera.to_json() for camera in cameras]}


class Camera(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("model_name", type=str, required=True)

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        camera_id = service.cameras.add_camera(args["model_name"])
        camera = service.cameras.get_camera_by_id(camera_id)
        cache.key.evict_same_path_keys()
        return camera.to_json()


class Events(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        events = service.events.get_events()
        return {"events": [event.to_json() for event in events]}


class Event(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("chinese_name", type=str, required=True)
    post_parser.add_argument("english_name", type=str)

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        event_id = service.events.add_event(args["chinese_name"], args["english_name"])
        event = service.events.get_event_by_id(event_id)
        cache.key.evict_same_path_keys()
        return event.to_json()


class Habitats(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        habitats = service.habitats.get_habitats()
        return {"habitats": [habitat.to_json() for habitat in habitats]}


class Habitat(resources.PerchMountResource):
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

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        habitat_id = service.habitats.add_habitat(
            args["chinese_name"],
            args["english_name"],
        )
        habitat = service.habitats.get_habitat_by_id(habitat_id)
        cache.key.evict_same_path_keys()
        return habitat.to_json()


class Layers(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        layers = service.layers.get_layers()
        return {"layers": [layer.to_json() for layer in layers]}


class Layer(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("name", type=str, required=True)

    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self, layer_id: int):
        layer = service.layers.get_layer_by_id(layer_id)
        return layer.to_json()

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        layer_id = service.layers.add_layer(args["name"])
        layer = service.layers.get_layer_by_id(layer_id)
        cache.key.evict_same_path_keys()
        return layer.to_json()


class MountTypes(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        mount_types = service.mount_types.get_mount_types()
        return {"mount_types": [mount_type.to_json() for mount_type in mount_types]}


class MountType(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("name", type=str, required=True)

    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self, mount_type_id: int):
        mount_type = service.mount_types.get_mount_type_by_id(mount_type_id)
        return mount_type.to_json()

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        layer_id = service.layers.add_layer(args["name"])
        layer = service.layers.get_layer_by_id(layer_id)
        cache.key.evict_same_path_keys()
        return layer.to_json()


class Projects(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        projects = service.projects.get_projects()
        return {"projects": [project.to_json() for project in projects]}


class Project(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("name", type=str, required=True)

    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self, project_id: int):
        project = service.projects.get_project_by_id(project_id)
        return project.to_json()

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        project_id = service.projects.add_project(args["name"])
        project = service.projects.get_project_by_id(project_id)
        cache.key.evict_same_path_keys()
        return project.to_json()


class Positions(resources.PerchMountResource):
    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        positions = service.positions.get_positions()
        return {"positions": [position.to_json() for position in positions]}


class Position(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("name", type=str, required=True)

    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self, position_id: int):
        postion = service.positions.get_position_by_id(position_id)
        return postion.to_json()

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        position_id = service.positions.add_position(args["name"])
        position = service.positions.get_position_by_id(position_id)
        cache.key.evict_same_path_keys()
        return position.to_json()
