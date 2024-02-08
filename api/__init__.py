import datetime
import flask_restful

TRUES = {"true", "1", "yes", "y"}


def _query_bool(phase: str) -> bool:
    return phase.lower() in TRUES


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
    "project": int,
    "habitat": int,
    "terminated": _query_bool,
    "claim_by": int,
    "perch_mount": int,
    "check_date_from": datetime.datetime.fromisoformat,
    "check_date_to": datetime.datetime.fromisoformat,
    "operator": int,
}


class PerchMountResource(flask_restful.Resource):
    def _correct_types(self, args: dict) -> dict:

        for k, v in TYPE_MAP.items():
            if k in args:
                args[k] == v(args[k])

        return args
