import flask
import flask_restful.reqparse

import api
import service.members as ServiceMembers


class Members(api.PerchMountResource):
    def get(self):
        results = ServiceMembers.get_members()
        return {"members": [result.to_json() for result in results]}


class Member(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("user_name", type=str, required=True)
    post_parser.add_argument("first_name", type=str, required=True)
    post_parser.add_argument("last_name", type=str, required=True)
    post_parser.add_argument("position", type=int, required=True)
    post_parser.add_argument("phone_number", type=str, required=True)
    post_parser.add_argument("is_admin", type=bool, required=True)
    patch_parser = flask_restful.reqparse.RequestParser()
    patch_parser.add_argument("user_name", type=str)
    patch_parser.add_argument("first_name", type=str)
    patch_parser.add_argument("last_name", type=str)
    patch_parser.add_argument("position", type=int)
    patch_parser.add_argument("phone_number", type=str)
    patch_parser.add_argument("is_admin", type=bool)

    def get(self, member_id: int):
        member = ServiceMembers.get_member_by_id(member_id)
        return member.to_json()

    def patch(self, memeber_id: int):
        self.patch_parser.parse_args(strict=True)
        args = flask.request.get_json()
        ServiceMembers.update_member(memeber_id, args)
        member = ServiceMembers.get_member_by_id(memeber_id)
        return member.to_json()

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        member_id = ServiceMembers.add_member(**args)
        member = ServiceMembers.get_member_by_id(member_id)
        return member.to_json()
