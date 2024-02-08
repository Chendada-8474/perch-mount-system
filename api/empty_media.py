import flask
import api
import flask_restful.reqparse

import service.empty_media as ServiceEmptyMedia


class EmptyMedia(api.PerchMountResource):
    post_parser = flask_restful.reqparse.RequestParser()
    post_parser.add_argument("media", type=list[dict], required=True, location="json")

    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        media = ServiceEmptyMedia.get_empty_media(**args)
        return {"media": [medium.to_json() for medium in media]}

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        ServiceEmptyMedia.add_empty_media(args["media"])
        return {"message": "success"}
