import flask_restful


class BasicMedia(flask_restful.Resource):
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
