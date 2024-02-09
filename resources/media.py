import flask
import flask_restful.reqparse

import resources
import service.media as ServiceMedia


class Media(resources.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("media", type=list[dict], required=True, location="json")
    put_parser = flask_restful.reqparse.RequestParser()
    put_parser.add_argument("media", type=list[dict], required=True, location="json")
    put_parser.add_argument(
        "detected_indices", type=list[str], required=True, location="json"
    )

    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        media = ServiceMedia.get_media(**args)
        return {"media": [medium.to_json() for medium in media]}

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        ServiceMedia.add_media_individuals(args["media"])

    def put(self):
        args = self.put_parser.parse_args(strict=True)
        ServiceMedia.review(args["detected_indices"], args["media"])


class Medium(flask_restful.Resource):
    def get(self, medium_id: str):
        medium = ServiceMedia.get_medium_by_id(medium_id)
        return medium.to_json()

    def patch(self):
        return
