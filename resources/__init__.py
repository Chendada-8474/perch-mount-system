import datetime
import flask_restful

__all__ = [
    "detected_media",
    "empty_media",
    "media",
    "members",
    "options",
    "perch_mounts",
    "sections",
    "species",
]


TRUES = {"true", "1", "yes", "y", "ya"}


def _query_bool(phase: str) -> bool:
    return phase.lower() in TRUES


TYPE_MAP = (
    ("section", int),
    ("perch_mount", int),
    ("offset", int),
    ("limit", int),
    ("section_id", int),
    ("perch_mount_id", int),
    ("taxon_order", int),
    ("category", str),
    ("order", str),
    ("family", str),
    ("prey", _query_bool),
    ("project", int),
    ("habitat", int),
    ("terminated", _query_bool),
    ("claim_by", int),
    ("perch_mount", int),
    ("check_date_from", datetime.datetime.fromisoformat),
    ("check_date_to", datetime.datetime.fromisoformat),
    ("operator", int),
)


class PerchMountResource(flask_restful.Resource):
    def _correct_types(self, args: dict) -> dict:
        for colname, type in TYPE_MAP:
            if colname in args:
                args[colname] = type(args[colname])
        return args
