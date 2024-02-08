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

    def post(self):
        return


class Cameras(api.PerchMountResource):
    def get(self):
        return

    def post(self):
        return


class Events(api.PerchMountResource):
    def get(self):
        return

    def post(self):
        return


class Habitats(api.PerchMountResource):
    def get(self):
        return

    def post(self):
        return


class Layers(api.PerchMountResource):
    def get(self):
        return

    def post(self):
        return


class MountTypes(api.PerchMountResource):
    def get(self):
        return

    def post(self):
        return


class Projects(api.PerchMountResource):
    def get(self):
        return

    def post(self):
        return


class Positions(api.PerchMountResource):
    def get(self):
        return

    def post(self):
        return
