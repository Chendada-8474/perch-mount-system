import flask_restful


def _query_bool(phase: str) -> bool:
    phase = phase.lower()
    return phase == "true" or phase == "1"


TYPE_MAP = {
    "section": int,
    "perch_mount": int,
    "offset": int,
    "limit": int,
    "section_id": int,
    "perch_mount_id": int,
    "taxon_order": int,
    "category": str,
    "order": str,
    "family": str,
    "prey": _query_bool,
}


class BasicMedia(flask_restful.Resource):
    def _correct_types(self, args: dict) -> dict:

        for k, v in TYPE_MAP.items():
            if k in args:
                args[k] == v(args[k])

        return args
