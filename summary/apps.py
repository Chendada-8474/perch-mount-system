import flask
import service.perch_mounts
import service.members
import resources.utils


blueprint = flask.Blueprint("summary", __name__)


@blueprint.route("/perch_mounts/<int:perch_mount_id>/media_count")
def media_count(perch_mount_id: int):
    results = service.perch_mounts.section_media_count(perch_mount_id)
    print(results)
    return flask.jsonify(results)


@blueprint.route("/perch_mounts/pending")
def pending_perch_mounts():

    results = service.perch_mounts.perch_mounts_pending_media_count()
    member_indice = [result.claim_by for result in results if result.claim_by]
    members = service.members.get_member_by_indice(member_indice)
    members = [member.to_json() for member in members]
    return {
        "perch_mounts": [result._asdict() for result in results],
        "members": resources.utils.field_as_key(members, "member_id"),
    }
