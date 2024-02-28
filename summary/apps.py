import flask

from service import perch_mounts

blueprint = flask.Blueprint("summary", __name__)


@blueprint.route("/perch_mounts/<int:perch_mount_id>/media_count")
def media_count(perch_mount_id: int):
    results = perch_mounts.section_media_count(perch_mount_id)
    return flask.jsonify(results)
