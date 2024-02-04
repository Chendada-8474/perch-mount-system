from flask import Flask
from flask_restful import Api
from service import SQLALCHEMY_DATABASE_URI
import api.perch_mounts as APIPerchMounts
import api.sections as APISections
import api.empty_media as APIEmptyMedia
import api.detected_media as APIDetectedMedia

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

api = Api(app)


api.add_resource(APIPerchMounts.PerchMounts, "/perch_mounts")
api.add_resource(
    APIPerchMounts.PerchMount, "/perch_mounts/<int:perch_mount_id>", "/perch_mounts"
)
api.add_resource(APISections.Sections, "/sections")
api.add_resource(APISections.Section, "/sections/<int:section_id>", "/sections")
api.add_resource(APIEmptyMedia.EmptyMedia, "/empty_media")
api.add_resource(APIDetectedMedia.DetectedMedia, "/detected_media")


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
