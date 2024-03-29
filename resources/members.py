import flask
import flask_restful.reqparse
import flask_jwt_extended

import cache
import cache.key
import resources
import service.members


class Members(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("user_name", type=str, required=True)
    post_parser.add_argument("first_name", type=str, required=True)
    post_parser.add_argument("last_name", type=str, required=True)
    post_parser.add_argument("position", type=int, required=True)
    post_parser.add_argument("phone_number", type=str, required=True)
    post_parser.add_argument("is_admin", type=bool, required=True)

    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self):
        results = service.members.get_members()
        return {"members": [result._asdict() for result in results]}

    @flask_jwt_extended.jwt_required()
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        member_id = service.members.add_member(**args)
        member = service.members.get_member_by_id(member_id)
        cache.key.evict_same_path_keys()
        return member.to_json()


class Member(resources.PerchMountResource):
    patch_parser = flask_restful.reqparse.RequestParser()
    patch_parser.add_argument("user_name", type=str)
    patch_parser.add_argument("first_name", type=str)
    patch_parser.add_argument("last_name", type=str)
    patch_parser.add_argument("position", type=int)
    patch_parser.add_argument("phone_number", type=str)
    patch_parser.add_argument("is_admin", type=bool)

    @flask_jwt_extended.jwt_required()
    @cache.cache.cached(make_cache_key=cache.key.key_generate)
    def get(self, member_id: int):
        member = service.members.get_member_by_id(member_id)
        return member.to_json()

    @flask_jwt_extended.jwt_required()
    def patch(self, member_id: int):
        self.patch_parser.parse_args(strict=True)
        args = flask.request.get_json()
        service.members.update_member(member_id, args)
        member = service.members.get_member_by_id(member_id)
        cache.key.evict_same_path_keys()
        return member.to_json()
