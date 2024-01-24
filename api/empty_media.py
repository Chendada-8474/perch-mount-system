from datetime import datetime, date
import flask
import flask_restful
from flask_restful import reqparse

from api import utils
import service.empty_media as ServiceEmptyMedia


class EmptyMedia(flask_restful.Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument("media", action="append")

    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        media = ServiceEmptyMedia.get_empty_media(**args)
        return {"media": [medium.to_json() for medium in media]}

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        ServiceEmptyMedia.add_empty_media(args.media)

    def _correct_types(self, args: dict) -> dict:
        if "section" in args:
            args["section"] == int(args["section"])
        if "perch_mount" in args:
            args["perch_mount"] == int(args["perch_mount"])
        if "offset" in args:
            args["offset"] = int(args["offset"])
        if "limit" in args:
            args["limit"] == int(args["limit"])
        return args
