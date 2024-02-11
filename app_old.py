import os
from PIL import Image
from io import BytesIO
from src.model import db, migrate
from src.login import login_manager
import configs.mysql
import configs.path
import configs.config as config
import configs.api_urls as api_urls
import src.login
import src.form as form
import src.file as file
import src.data_request as req

from flask_caching import Cache
from flask_restful import Api
from flaskext.markdown import Markdown
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
import src.resources.prey as res_prey
import src.resources.media as res_media
import src.resources.member as res_member
import src.resources.section as res_section
import src.resources.options as res_options
import src.resources.individual as res_individual
import src.resources.perch_mount as res_perch_mount
import src.resources.contribution as res_contribution
import src.resources.featured as res_featured
import src.resources.update_info as res_update
import src.resources.row_data as res_row

HOST = "http://127.0.0.1:5000"

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://%s:%s@%s:%s/%s" % (
    configs.mysql.master_user,
    configs.mysql.master_passward,
    configs.mysql.master_ip,
    configs.mysql.master_port,
    configs.mysql.database,
)

app.config.from_mapping(config.cache)

api = Api(app)
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
Markdown(app)
cache = Cache(app)

encryptor = file.Encryptor()


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
    updates = req.get("/api/updates")

    project_form = form.NewProject()
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
        project_form=project_form,
        updates=updates,
    )


@app.route("/perch_mount/<int:perch_mount_id>")
@login_required
def perch_mount(perch_mount_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")

    if not perch_mount_:
        return render_template("404.html")

    sections = req.get(f"/api/perch_mount/{perch_mount_id}/sections")
    media_count = req.get(f"/api/perch_mount/{perch_mount_id}/media_count")
    projects_ = req.get(f"/api/projects")
    habitats_ = req.get(f"/api/habitats")
    members_ = req.get(f"/api/members")

    total = (
        media_count["count"]
        + media_count["detected_count"]
        + media_count["empty_count"]
    )
    complete_rate = round(media_count["count"] / total * 100, 2) if total else None

    month_empty_count = req.get(
        f"/api/perch_mount/{perch_mount_id}/month_pending_empty_count"
    )
    month_detected_count = req.get(
        f"/api/perch_mount/{perch_mount_id}/month_pending_detected_count"
    )
    section_prey_count = req.get(f"/api/perch_mount/{perch_mount_id}/section_preys")

    return render_template(
        "perch_mount.html",
        perch_mount=perch_mount_,
        sections=sections,
        projects=projects_,
        habitats=habitats_,
        members=members_,
        media_count=media_count,
        month_empty_count=month_empty_count,
        month_detected_count=month_detected_count,
        section_prey_count=section_prey_count,
        complete_rate=complete_rate,
    )


@app.route("/perch_mount/<int:perch_mount_id>/section/<int:section_id>")
@cache.cached(timeout=600)
@login_required
def section(perch_mount_id: int, section_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    section_ = req.get(f"api/section/{section_id}")
    media = req.get(f"/api/section/{section_id}/media")
    empty_media = req.get(f"/api/section/{section_id}/empty_media")
    detected_media = req.get(f"/api/section/{section_id}/detected_media")

    detected_media = file.add_all_file_name(detected_media)
    empty_media = file.add_all_file_name(empty_media)
    media = file.add_all_file_name(media)

    return render_template(
        "section.html",
        perch_mount=perch_mount_,
        section=section_,
        media=media,
        empty_media=empty_media,
        detected_media=detected_media,
    )


@app.route(
    "/perch_mount/<int:perch_mount_id>/section/<int:section_id>/medium/<string:medium_id>"
)
@login_required
def medium_page(perch_mount_id: int, section_id: int, medium_id: str):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    section_ = req.get(f"api/section/{section_id}")
    medium = req.get(f"/api/medium/{medium_id}")
    individuals = req.get(f"/api/medium/{medium_id}/individuals")
    events_ = req.get(f"/api/events")
    behaviors_ = req.get("/api/behaviors")

    medium = file.add_is_image(medium)
    medium = file.add_file_name(medium)
    medium["epath"] = encryptor.encrypt(medium["path"])

    return render_template(
        "medium.html",
        perch_mount=perch_mount_,
        section=section_,
        medium=medium,
        individuals=individuals,
        events=events_,
        behaviors=behaviors_,
    )


@app.route("/empty_check/perch_mount/<int:perch_mount_id>")
@login_required
def empty_check_perch_mount(perch_mount_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    media = req.get(
        f"/api/empty_check/perch_mount/{perch_mount_id}/limit/{config.EMPTY_CHECK_LIMIT}"
    )
    media = file.add_all_is_image(media)

    for medium in media:
        medium["epath"] = encryptor.encrypt(medium["path"])

    return render_template(
        "empty_check.html",
        media=media,
        perch_mount=perch_mount_,
    )


@app.route("/empty_check/perch_mount/<int:perch_mount_id>/section/<int:section_id>")
@login_required
def empty_check_section(perch_mount_id: int, section_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    media = req.get(
        f"/api/empty_check/section/{section_id}/limit/{config.EMPTY_CHECK_LIMIT}"
    )
    media = file.add_all_is_image(media)

    for medium in media:
        medium["epath"] = encryptor.encrypt(medium["path"])

    return render_template(
        "empty_check.html",
        media=media,
        perch_mount=perch_mount_,
    )


@app.route("/review/perch_mount/<int:perch_mount_id>/section/<int:section_id>")
@login_required
def review_section(perch_mount_id: int, section_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    behaviors = req.get("/api/behaviors")
    events_ = req.get("/api/events")
    media = req.get(f"/api/review/section/{section_id}/limit/{config.REVIEW_LIMIT}")
    media = file.add_all_is_image(media)
    media = file.add_all_file_name(media)

    for medium in media:
        medium["epath"] = encryptor.encrypt(medium["path"])

    return render_template(
        "review.html",
        behaviors=behaviors,
        events=events_,
        media=media,
        perch_mount=perch_mount_,
    )


@app.route("/review/perch_mount/<int:perch_mount_id>")
@login_required
def review_perch_mount(perch_mount_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    behaviors = req.get("/api/behaviors")
    events_ = req.get("/api/events")
    media = req.get(
        f"/api/review/perch_mount/{perch_mount_id}/limit/{config.REVIEW_LIMIT}"
    )
    media = file.add_all_is_image(media)
    media = file.add_all_file_name(media)

    for medium in media:
        medium["epath"] = encryptor.encrypt(medium["path"])

    return render_template(
        "review.html",
        behaviors=behaviors,
        events=events_,
        media=media,
        perch_mount=perch_mount_,
    )


@app.route("/review/perch_mount/<int:perch_mount_id>/year_month/<string:year_month>")
@login_required
def review_month_perch_mount(perch_mount_id: int, year_month: str):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    behaviors = req.get("/api/behaviors")
    events_ = req.get("/api/events")
    media = req.get(
        f"/api/review/perch_mount/{perch_mount_id}/year_month/{year_month}/limit/{config.REVIEW_LIMIT}"
    )
    media = file.add_all_is_image(media)
    media = file.add_all_file_name(media)

    for medium in media:
        medium["epath"] = encryptor.encrypt(medium["path"])

    return render_template(
        "review.html",
        behaviors=behaviors,
        events=events_,
        media=media,
        perch_mount=perch_mount_,
    )


@app.route(
    "/empty_check/perch_mount/<int:perch_mount_id>/year_month/<string:year_month>"
)
@login_required
def empty_check_month_perch_mount(perch_mount_id: int, year_month: str):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    media = req.get(
        f"/api/empty_check/perch_mount/{perch_mount_id}/year_month/{year_month}/limit/{config.REVIEW_LIMIT}"
    )
    media = file.add_all_is_image(media)

    for medium in media:
        medium["epath"] = encryptor.encrypt(medium["path"])

    return render_template(
        "empty_check.html",
        media=media,
        perch_mount=perch_mount_,
    )


@app.route(
    "/empty_check_detected/perch_mount/<int:perch_mount_id>/section/<int:section_id>"
)
@login_required
def empty_check_detected_section(perch_mount_id: int, section_id: int):
    perch_mount_ = req.get(f"/api/perch_mount/{perch_mount_id}")
    media = req.get(
        f"/api/empty_check_detected/section/{section_id}/limit/{config.DETECTED_EMPTY_CHECK_LIMIT}"
    )
    media = file.add_all_is_image(media)

    for medium in media:
        medium["epath"] = encryptor.encrypt(medium["path"])

    print(perch_mount_)

    return render_template(
        "detected_empty_check.html",
        media=media,
        perch_mount=perch_mount_,
        section_id=section_id,
    )


@app.route(
    "/identify_prey/<string:predator>/perch_mount/<int:perch_mount_id>/section/section/<int:section_id>"
)
@login_required
def identify_prey(perch_mount_id: int, section_id: int, predator: str):
    perch_mount_ = req.get(f"api/perch_mount/{perch_mount_id}")

    media = req.get(f"/api/identify_prey/{predator}/section/{section_id}")
    media = file.add_all_is_image(media)
    media = file.add_all_file_name(media)

    for medium in media:
        medium["epath"] = encryptor.encrypt(medium["path"])

    return render_template("identify_prey.html", media=media, perch_mount=perch_mount_)


@app.route(
    "/featured/page/<int:page>/perch_mount/<string:perch_mount_name>/behavior/<int:behavior_id>/species/<string:chinese_common_name>/member/<int:member_id>"
)
@login_required
def featured(
    page: int,
    perch_mount_name: str,
    behavior_id: int,
    chinese_common_name: str,
    member_id: int,
):
    media = req.get(
        f"/api/featured/page/{page}/perch_mount/{perch_mount_name}/behavior/{behavior_id}/species/{chinese_common_name}/member/{member_id}"
    )
    behaviors_ = req.get("/api/behaviors")
    perch_mounts_ = req.get("/api/perch_mounts")
    species_ = req.get("/api/species")
    members_ = req.get("/api/members")

    media["media"] = file.add_all_file_name(media["media"])
    media["media"] = file.add_all_is_image(media["media"])

    for medium in media["media"]:
        medium["epath"] = encryptor.encrypt(medium["path"])

    num_page = (media["count"] - 1) // config.NUM_MEDIA_IN_PAGE + 1
    first_page = max(page - 6, 0)
    end_page = min(page + 6, num_page)

    return render_template(
        "featured.html",
        behaviors=behaviors_,
        perch_mounts=perch_mounts_,
        species=species_,
        members=members_,
        media=media["media"],
        page=page,
        first_page=first_page,
        end_page=end_page,
        num_page=num_page,
        perch_mount_name=perch_mount_name,
        behavior_id=behavior_id,
        member_id=member_id,
        chinese_common_name=chinese_common_name,
        total=media["count"],
    )


@app.route("/pending")
@login_required
def pending():
    pendings = req.get("/api/pending_perch_mounts")
    projects = req.get("/api/projects")

    total_empty = sum(p["empty_count"] for p in pendings if p["empty_count"])
    total_detected = sum(p["detected_count"] for p in pendings if p["detected_count"])
    ai_tasks = os.listdir(configs.path.TASKS_DIR_PATH)
    return render_template(
        "pending.html",
        pendings=pendings,
        projects=projects,
        ai_tasks=ai_tasks,
        total_empty=total_empty,
        total_detected=total_detected,
    )


@app.route("/parameter")
@cache.cached(timeout=3600)
@login_required
def parameter_maker():
    perch_mounts_ = req.get("/api/perch_mounts")
    mount_types_ = req.get("/api/mount_types")
    cameras_ = req.get("/api/cameras")
    members_ = req.get("/api/members")

    parameter_form = form.Parameter()
    parameter_form.init_choice(mount_types_, cameras_, members_)

    return render_template(
        "parameter.html",
        mount_types=mount_types_,
        parameter_form=parameter_form,
        perch_mounts=perch_mounts_,
    )


@app.route("/members")
@login_required
def members():
    members_ = req.get("/api/members")
    positions = req.get("/api/positions")
    member_form = form.NewMember()
    member_form.init_choices(
        positions=[(p["position_id"], p["name"]) for p in positions]
    )

    return render_template(
        "members.html",
        members=members_,
        member_form=member_form,
    )


@app.route("/member/<int:member_id>")
@login_required
def member_page(member_id: int):
    member = req.get(f"/api/member/{member_id}")
    contributions = req.get(f"/api/member/{member_id}/contributions")
    perch_mounts = req.get(f"/api/member/{member_id}/perch_mounts")
    return render_template(
        "member.html",
        member=member,
        contributions=contributions,
        perch_mounts=perch_mounts,
    )


@app.route("/behaviors")
@login_required
def behaviors():
    behaviors_ = req.get("/api/behaviors")
    behavior_form = form.NewBehavior()

    return render_template(
        "behavior.html",
        behaviors=behaviors_,
        behavior_form=behavior_form,
    )


@app.route("/cameras")
@login_required
def cameras():
    cameras_ = req.get("/api/cameras")
    camera_form = form.NewCamera()

    return render_template(
        "camera.html",
        cameras=cameras_,
        camera_form=camera_form,
    )


@app.route("/events")
@login_required
def events():
    events_ = req.get("/api/events")
    event_form = form.NewEvent()

    return render_template(
        "event.html",
        events=events_,
        event_form=event_form,
    )


@app.route("/species")
@cache.cached(timeout=3600)
@login_required
def species_page():
    species = req.get("/api/species")

    return render_template("species.html", species=species)


@app.route("/update_info")
@cache.cached(timeout=3600)
@login_required
def update_info():
    updates = req.get("/api/updates")

    return render_template("update_info.html", updates=updates)


@app.route("/download")
@cache.cached(timeout=3600)
@login_required
def download():
    data_form = form.RowData()

    projects = req.get("/api/projects")
    record_species = req.get("/api/record_species")
    data_form.init_choice(projects, record_species)

    return render_template("download.html", data_form=data_form)


@app.route("/uploads/<path:path>")
def send_media(path):
    path = encryptor.decrypt(path)
    _, extension = os.path.splitext(path)
    if extension.lower()[1:] in config.IMAGE_EXTENSIONS:
        try:
            image_io = BytesIO()
            image = Image.open(path)
            image.thumbnail((960, 540))
            image.save(image_io, "JPEG")
            image_io.seek(0)
            return send_file(image_io, mimetype="image/jpeg")
        except:
            return send_from_directory("./static/img", "not_found.png")

    elif extension.lower()[1:] in config.VIDEO_EXTENSIONS:
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return send_from_directory(dir_path, file_name)


@app.route("/download_medium/<string:medium_id>", methods=["GET", "POST"])
def download_medium(medium_id: str):
    medium_ = req.get(f"/api/medium/{medium_id}")
    return send_file(medium_["path"], as_attachment=True)


api.add_resource(res_perch_mount.PerchMounts, api_urls.PERCH_MOUNTS)
api.add_resource(
    res_perch_mount.PerchMount, api_urls.PERCH_MOUNT1, api_urls.PERCH_MOUNT2
)
api.add_resource(res_perch_mount.ClaimedPerchMounts, api_urls.PERCH_MOUNTS_CLAIM_BY)
api.add_resource(res_perch_mount.PerchMountMediaCount, api_urls.PERCH_MOUNT_MEDIA_COUNT)
api.add_resource(res_perch_mount.PendingPerchMounts, api_urls.PENDING_PERCH_MOUNTS)
api.add_resource(
    res_perch_mount.PerchMountClaimBy,
    api_urls.PERCH_MOUNT_CLAIM_BY1,
    api_urls.PERCH_MOUNT_CLAIM_BY2,
)
api.add_resource(
    res_perch_mount.PerchMountMonthPendingEmptyCount,
    api_urls.PERCH_MOUNT_MONTH_PENDING_EMPTY_COUNT,
)
api.add_resource(
    res_perch_mount.PerchMountMonthPendingDetectedCount,
    api_urls.PERCH_MOUNT_MONTH_PENDING_DETECTED_COUNT,
)
api.add_resource(res_prey.PerchMountSectionPreyCount, api_urls.PERCH_MOUNT_PREY_COUNT)

# api.add_resource(res_media.EmptyMedia, api_urls.)
api.add_resource(res_media.EmptyDayCountOfPerchMount, api_urls.EMPTY_DAY_COUNT)
api.add_resource(res_media.DetectedDayCountOfPerchMount, api_urls.DETECTED_DAY_COUNT)

api.add_resource(res_media.EmptyCheckSection, api_urls.EMPTY_CHECK_SECTION)
api.add_resource(
    res_media.EmptyCheckPerchMount,
    api_urls.EMPTY_CHECK_PERCH_MOUNT_1,
    api_urls.EMPTY_CHECK_PERCH_MOUNT_2,
)
api.add_resource(
    res_media.EmptyCheckMonthPerchMount,
    api_urls.EMPTY_CHECK_MONTH_PERCH_MOUNT_,
)

api.add_resource(
    res_media.DetectedUnCheckedSectionMedia,
    api_urls.EMPTY_CHECK_DETECTED_MEDIA_1,
    api_urls.EMPTY_CHECK_DETECTED_MEDIA_2,
)

api.add_resource(res_media.ReviewSection, api_urls.REVIEW_SECTION)
api.add_resource(
    res_media.ReviewPerchMount,
    api_urls.REVIEW_PERCH_MOUNT_1,
    api_urls.REVIEW_PERCH_MOUNT_2,
)
api.add_resource(
    res_media.ReviewMonthPerchMount,
    api_urls.REVIEW_MONTH_PERCH_MOUNT_,
)

api.add_resource(res_prey.IdentifySectionPreys, api_urls.IDENTIFY_PREY_SECTION)

api.add_resource(res_media.Medium, api_urls.MEDIUM)
api.add_resource(res_media.SectionMedia, api_urls.SECTION_MEDIA)
api.add_resource(res_media.SectionEmptyMedia, api_urls.SECTION_EMPTY_MEDIA)
api.add_resource(res_media.SectionDetectedMedia, api_urls.SECTION_DETECTED_MEDIA)

api.add_resource(res_individual.IndividualsOfMedium, api_urls.MEDIUM_INDIVIDUALS)
api.add_resource(res_individual.Individual, api_urls.INDIVIDUAL1, api_urls.INDIVIDUAL2)

api.add_resource(res_options.AllBehaviors, api_urls.BEHAVIORS)
api.add_resource(res_options.Positions, api_urls.POSITIONS)
api.add_resource(res_options.Habitats, api_urls.HABITATS)
api.add_resource(res_options.AllCameras, api_urls.CAMERAS)
api.add_resource(res_options.AllEvents, api_urls.EVENTS)
api.add_resource(res_options.Layers, api_urls.LAYERS)
api.add_resource(res_options.MountTypes, api_urls.MOUNT_TYPES)
api.add_resource(res_options.Projects, api_urls.PROJECTS)
api.add_resource(res_options.Project, api_urls.PROJECT)
api.add_resource(res_options.AllSpecies, api_urls.SPECIES)

api.add_resource(res_options.Behavior, api_urls.BEHAVIOR)
api.add_resource(res_options.Camera, api_urls.CAMERA)
api.add_resource(res_options.Event, api_urls.EVENT)

api.add_resource(res_options.SpeciesTrie, api_urls.SPECIES_SEARCH)
api.add_resource(res_options.SpeciesTaxonOrders, api_urls.SPECIES_TAXON_ORDERS)

api.add_resource(res_section.OneSection, api_urls.SECTION1, api_urls.SECTION2)
api.add_resource(res_section.SectionsOfPerchMount, api_urls.PERCH_MOUNT_SECTIONS)
api.add_resource(res_section.OperatorsOfSection, api_urls.SECTION_OPERATORS)

api.add_resource(res_member.AllMembers, api_urls.MEMBERS)
api.add_resource(res_member.Member, api_urls.MEMBER1, api_urls.MEMBER2)
api.add_resource(res_member.MemberContributions, api_urls.MEMBER_CONTRIBUTIONS)

api.add_resource(res_contribution.Contribution, api_urls.CONTRIBUTION)

api.add_resource(res_prey.Prey, api_urls.PREY)
api.add_resource(res_featured.FeaturedMedia, api_urls.FEATURED_MEDIA)
api.add_resource(res_featured.FeaturedMedium, api_urls.FEATURD_MEDIUM)

api.add_resource(res_media.ScheduleDetectMedia, api_urls.SCHEDULE_DETECT_MEDIA)

api.add_resource(res_update.UpdateInfo, api_urls.UPDATE_INFO1, api_urls.UPDATE_INFO2)
api.add_resource(res_update.UpdateInfos, api_urls.ALL_UPDATE_INFO)

api.add_resource(res_row.RowData, api_urls.QUERY_DATA)
api.add_resource(res_options.RecordSpecies, api_urls.RECORD_SPECIES)
api.add_resource(res_media.ProcessedMedia, api_urls.PROCESSED_DATA)
api.add_resource(res_contribution.ScheduleDetectCount, api_urls.SCHEDULE_DETECT_COUNT)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
