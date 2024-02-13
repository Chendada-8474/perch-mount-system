import flask
from flask_restful import reqparse

import resources
import service.detected_media as ServiceDetectedMedia


class DetectedMedia(resources.PerchMountResource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        "detected_media", type=list[dict], required=True, location="json"
    )
    put_parser = reqparse.RequestParser()
    put_parser.add_argument(
        "detected_media", type=list[dict], required=True, location="json"
    )
    put_parser.add_argument(
        "empty_indices", type=list[str], required=True, location="json"
    )

    def get(self):
        args = dict(flask.request.args)
        args = self._correct_types(args)
        media = ServiceDetectedMedia.get_detected_media(**args)
        return {"media": [medium.to_json() for medium in media]}

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        ServiceDetectedMedia.add_media_individuals(args["detected_media"])

    def put(self):
        args = self.put_parser.parse_args(strict=True)
        ServiceDetectedMedia.detect(args["empty_indices"], args["detected_media"])
