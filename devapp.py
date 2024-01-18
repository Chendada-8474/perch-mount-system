from flask import Flask
from flask_restful import Api
from service import SQLALCHEMY_DATABASE_URI
from api.perch_mounts import PerchMounts, PerchMount
from api.sections import Sections

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

api = Api(app)


api.add_resource(PerchMounts, "/perch_mounts")
api.add_resource(PerchMount, "/perch_mounts/<int:perch_mount_id>", "/perch_mounts")
api.add_resource(Sections, "/sections")


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
