from flask import Flask
from flask_restful import Api
from src.model import db, migrate
from urllib.parse import urljoin
import requests
import configs.mysql
import configs.api_urls as api_urls
import src.resources.perch_mount as res_perch_mount
import src.resources.section as res_section
import src.resources.media as res_media
import src.resources.individual as res_individual
import src.resources.options as res_options

HOST = "http://127.0.0.1:5000"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://%s:%s@%s:3306/%s" % (
    configs.mysql.user,
    configs.mysql.passward,
    configs.mysql.ip,
    configs.mysql.database,
)

api = Api(app)
db.init_app(app)
migrate.init_app(app, db)


@app.route("/")
def hello_world():
    response = requests.get(urljoin(HOST, "/api/section/3/media"))
    return "<p>%s</p>" % response.json()


api.add_resource(
    res_perch_mount.PerchMount, api_urls.PERCH_MOUNT1, api_urls.PERCH_MOUNT2
)

api.add_resource(res_section.SectionsOfPerchMount, api_urls.SECTIONS_OF_PERCH_MOUNT)

api.add_resource(res_media.EmptyMedia, api_urls.SECTIONS_OF_PERCH_MOUNT)

api.add_resource(res_media.EmptyDayCountOfPerchMount, api_urls.EMPTY_DAY_COUNT)
api.add_resource(res_media.DetectedDayCountOfPerchMount, api_urls.DETECTED_DAY_COUNT)

api.add_resource(
    res_media.EmptyCheckMedia, api_urls.EMPTY_CHECK1, api_urls.EMPTY_CHECK2
)
api.add_resource(res_media.ReviewMedia, api_urls.REVIEW1, api_urls.REVIEW2)

api.add_resource(res_media.Medium, api_urls.MEDIUM)
api.add_resource(res_media.SectionMedia, api_urls.SECTION_MEDIA)
api.add_resource(res_individual.IndividualOfMedium, api_urls.MEDIUM_INDIVIDUALS)

api.add_resource(res_individual.Individual, api_urls.INDIVIDUAL)

api.add_resource(res_options.Positions, api_urls.POSITIONS)
api.add_resource(res_options.Habitats, api_urls.HABITATS)
api.add_resource(res_options.Cameras, api_urls.CAMERAS)
api.add_resource(res_options.Events, api_urls.EVENTS)
api.add_resource(res_options.Layers, api_urls.LAYERS)
api.add_resource(res_options.MountTypes, api_urls.MOUNT_TYPES)
api.add_resource(res_options.Projects, api_urls.PROJECTS)

api.add_resource(res_section.OperatorsOfSection, api_urls.SECTION_OPERATORS)
api.add_resource(res_perch_mount.ClaimedPerchMounts, api_urls.PERCH_MOUNT_CLAIM_BY)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
