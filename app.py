import os
from PIL import Image
from io import BytesIO
from src.model import db, migrate
from src.login import login_manager
import configs.mysql
import configs.config as config
import configs.api_urls as api_urls
import src.login
import src.form as form
import src.file as file
import src.data_request as req

from flask_restful import Api
from flask_login import login_required, login_user, logout_user
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    send_file,
    send_from_directory,
)

import src.resources.media as res_media
import src.resources.member as res_member
import src.resources.section as res_section
import src.resources.options as res_options
import src.resources.individual as res_individual
import src.resources.perch_mount as res_perch_mount
import src.resources.contribution as res_contribution

HOST = "http://127.0.0.1:5000"

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://%s:%s@%s:3306/%s" % (
    configs.mysql.user,
    configs.mysql.passward,
    configs.mysql.ip,
    configs.mysql.database,
)

api = Api(app)
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    users = src.login.get_users()
    user_name = request.form["user_name"]
    if (
        user_name in users
        and request.form["phone_number"] == users[user_name]["phone_number"]
    ):
        user = src.login.User()
        user.id = user_name
        login_user(user)
        return redirect(url_for("index"))
    return "Bad login"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    perch_mounts = req.get("/api/perch_mounts")
    projects = req.get("/api/projects")
    habitats = req.get("/api/habitats")
    layers = req.get("/api/layers")

    perch_mount_form = form.NewPerchMount()
    perch_mount_form.init_choices(
        habitats=[(h["habitat_id"], h["chinese_name"]) for h in habitats],
        projects=[(p["project_id"], p["name"]) for p in projects],
        layers=[("", "--")] + [(l["layer_id"], l["name"]) for l in layers],
    )

    return render_template(
        "index.html",
        perch_mounts=perch_mounts,
        projects=projects,
        habitats=habitats,
        layers=layers,
        perch_mount_form=perch_mount_form,
    )


@app.route("/perch_mount/<int:perch_mount_id>")
def perch_mount(perch_mount_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")

    if not perch_mount_:
        return render_template("404.html")

    sections = req.get(f"/api/perch_mount/{perch_mount_id}/sections")
    media_count = req.get(f"/api/perch_mount/{perch_mount_id}/media_count")

    total = (
        media_count["count"]
        + media_count["detected_count"]
        + media_count["empty_count"]
    )
    complete_rate = round(media_count["count"] / total * 100, 2) if total else None

    return render_template(
        "perch_mount.html",
        perch_mount=perch_mount_,
        sections=sections,
        media_count=media_count,
        complete_rate=complete_rate,
    )


@app.route("/perch_mount/<int:perch_mount_id>/section/<int:section_id>")
def section(perch_mount_id: int, section_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    section_ = req.get(f"api/section/{section_id}")
    media = req.get(f"/api/section/{section_id}/media")
    empty_media = req.get(f"/api/section/{section_id}/empty_media")
    detected_media = req.get(f"/api/section/{section_id}/detected_media")

    return render_template(
        "section.html",
        perch_mount=perch_mount_,
        section=section_,
        media=media,
        empty_media=empty_media,
        detected_media=detected_media,
    )


@app.route("/empty_check/perch_mount/<int:perch_mount_id>")
def empty_check_perch_mount(perch_mount_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    media = req.get(
        f"/api/empty_check/perch_mount/{perch_mount_id}/limit/{config.EMPTY_CHECK_LIMIT}"
    )
    media = file.add_is_image(media)
    return render_template(
        "empty_check.html",
        media=media,
        perch_mount=perch_mount_,
    )


@app.route("/empty_check/perch_mount/<int:perch_mount_id>/section/<int:section_id>")
def empty_check_section(perch_mount_id: int, section_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    media = req.get(
        f"/api/empty_check/section/{section_id}/limit/{config.EMPTY_CHECK_LIMIT}"
    )
    media = file.add_is_image(media)
    return render_template(
        "empty_check.html",
        media=media,
        perch_mount=perch_mount_,
    )


@app.route("/review/perch_mount/<int:perch_mount_id>/section/<int:section_id>")
def review_section(perch_mount_id: int, section_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    behaviors = req.get("/api/behaviors")
    events_ = req.get("/api/events")
    media = req.get(f"/api/review/section/{section_id}/limit/{config.REVIEW_LIMIT}")
    media = file.add_is_image(media)
    media = file.add_file_name(media)
    return render_template(
        "review.html",
        behaviors=behaviors,
        events=events_,
        media=media,
        perch_mount=perch_mount_,
    )


@app.route("/review/perch_mount/<int:perch_mount_id>")
def review_perch_mount(perch_mount_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    behaviors = req.get("/api/behaviors")
    events_ = req.get("/api/events")
    media = req.get(
        f"/api/review/perch_mount/{perch_mount_id}/limit/{config.REVIEW_LIMIT}"
    )
    media = file.add_is_image(media)
    media = file.add_file_name(media)
    return render_template(
        "review.html",
        behaviors=behaviors,
        events=events_,
        media=media,
        perch_mount=perch_mount_,
    )


@app.route("/pending")
def pending():
    pending_perch_mounts = req.get("api/pending_perch_mounts")
    projects = req.get("/api/projects")
    return render_template(
        "pending.html",
        pending_perch_mounts=pending_perch_mounts,
        projects=projects,
    )


@app.route("/members")
def members():
    members_ = req.get("/api/members")
    return render_template("member.html", members=members_)


@app.route("/uploads/<path:path>")
def send_media(path):
    _, extension = os.path.splitext(path)
    if extension.lower()[1:] in config.IMAGE_EXTENSIONS:
        image_io = BytesIO()
        image = Image.open(path)
        image.thumbnail((960, 540))
        image.save(image_io, "JPEG")
        image_io.seek(0)
        return send_file(image_io, mimetype="image/jpeg")
    elif extension.lower()[1:] in config.VIDEO_EXTENSIONS:
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return send_from_directory(dir_path, file_name)


api.add_resource(res_perch_mount.PerchMounts, api_urls.PERCH_MOUNTS)
api.add_resource(
    res_perch_mount.PerchMount, api_urls.PERCH_MOUNT1, api_urls.PERCH_MOUNT2
)
api.add_resource(res_perch_mount.ClaimedPerchMounts, api_urls.PERCH_MOUNT_CLAIM_BY)
api.add_resource(res_perch_mount.PerchMountMediaCount, api_urls.PERCH_MOUNT_MEDIA_COUNT)
api.add_resource(res_perch_mount.PendingPerchMounts, api_urls.PENDINGPERCHMOUNTS)

# api.add_resource(res_media.EmptyMedia, api_urls.)
api.add_resource(res_media.EmptyDayCountOfPerchMount, api_urls.EMPTY_DAY_COUNT)
api.add_resource(res_media.DetectedDayCountOfPerchMount, api_urls.DETECTED_DAY_COUNT)

api.add_resource(
    res_media.EmptyCheckPerchMount,
    api_urls.EMPTY_CHECK_PERCH_MOUNT_1,
    api_urls.EMPTY_CHECK_PERCH_MOUNT_2,
)
api.add_resource(
    res_media.ReviewPerchMount,
    api_urls.REVIEW_PERCH_MOUNT_1,
    api_urls.REVIEW_PERCH_MOUNT_2,
)
api.add_resource(res_media.EmptyCheckSection, api_urls.EMPTY_CHECK_SECTION)
api.add_resource(res_media.ReviewPerchSection, api_urls.REVIEW_SECTION)

api.add_resource(res_media.Medium, api_urls.MEDIUM)
api.add_resource(res_media.SectionMedia, api_urls.SECTION_MEDIA)
api.add_resource(res_media.SectionEmptyMedia, api_urls.SECTION_EMPTY_MEDIA)
api.add_resource(res_media.SectionDetectedMedia, api_urls.SECTION_DETECTED_MEDIA)

api.add_resource(res_individual.IndividualOfMedium, api_urls.MEDIUM_INDIVIDUALS)
api.add_resource(res_individual.Individual, api_urls.INDIVIDUAL)

api.add_resource(res_options.Behaviors, api_urls.BEHAVIORS)
api.add_resource(res_options.Positions, api_urls.POSITIONS)
api.add_resource(res_options.Habitats, api_urls.HABITATS)
api.add_resource(res_options.Cameras, api_urls.CAMERAS)
api.add_resource(res_options.Events, api_urls.EVENTS)
api.add_resource(res_options.Layers, api_urls.LAYERS)
api.add_resource(res_options.MountTypes, api_urls.MOUNT_TYPES)
api.add_resource(res_options.Projects, api_urls.PROJECTS)

api.add_resource(res_options.SpeciesTrie, api_urls.SPECIES_SEARCH)
api.add_resource(res_options.SpeciesTaxonOrders, api_urls.SPECIES_TAXON_ORDERS)

api.add_resource(res_section.OneSection, api_urls.SECTION)
api.add_resource(res_section.SectionsOfPerchMount, api_urls.SECTIONS_OF_PERCH_MOUNT)
api.add_resource(res_section.OperatorsOfSection, api_urls.SECTION_OPERATORS)

api.add_resource(res_member.AllMembers, api_urls.MEMBERS)
api.add_resource(res_member.Member, api_urls.MEMBER1, api_urls.MEMBER2)

api.add_resource(res_contribution.Contribution, api_urls.CONTRIBUTION)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
