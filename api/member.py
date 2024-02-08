import flask
import flask_restful.reqparse

import api
import service.members as ServiceMembers


class Members(api.PerchMountModel):
    def get(self):
        return


class Member(api.PerchMountModel):
    def get(self):
        return

    def post(self):
        return

    def patch(self):
        return
