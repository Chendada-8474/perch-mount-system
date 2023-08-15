from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


class JsonTable:
    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PerchMounts(db.Model, JsonTable):
    __tablename__ = "perch_mounts"
    perch_mount_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    perch_mount_name = db.Column(db.String(15), unique=True, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    habitat = db.Column(
        db.Integer, db.ForeignKey("habitats.habitat_id"), nullable=False
    )
    project = db.Column(
        db.Integer, db.ForeignKey("projects.project_id"), nullable=False
    )
    layer = db.Column(db.Integer, db.ForeignKey("layers.layer_id"))
    terminated = db.Column(db.Boolean, default=False)
    latest_note = db.Column(db.Text)
    is_priority = db.Column(db.Boolean)
    claim_by = db.Column(db.Integer, db.ForeignKey("members.member_id"))


class Sections(db.Model):
    __tablename__ = "sections"
    section_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    perch_mount = db.Column(db.Integer, db.ForeignKey("perch_mounts.perch_mount_id"))
    mount_type = db.Column(db.Integer, db.ForeignKey("mount_types.mount_type_id"))
    camera = db.Column(db.Integer, db.ForeignKey("cameras.camera_id"))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    check_date = db.Column(db.Date)
    valid = db.Column(db.Boolean)
    note = db.Column(db.Text)


class SectionOperators(db.Model):
    __tablename__ = "section_operaters"
    section = db.Column(
        db.Integer, db.ForeignKey("sections.section_id"), primary_key=True
    )
    operator = db.Column(
        db.Integer, db.ForeignKey("members.member_id"), primary_key=True
    )


class Media(db.Model):
    __tablename__ = "media"
    medium_id = db.Column(db.String(22), primary_key=True)
    section = db.Column(db.Integer, db.ForeignKey("sections.section_id"))
    medium_datetime = db.Column(db.DateTime)
    path = db.Column(db.String(255))
    empty_checker = db.Column(db.Integer, db.ForeignKey("members.member_id"))
    reviewer = db.Column(db.Integer, db.ForeignKey("members.member_id"))
    event = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    featured = db.Column(db.Boolean, default=False)
    featured_by = db.Column(db.Integer, db.ForeignKey("members.member_id"))
    featured_title = db.Column(db.String(100))
    featured_behavior = db.Column(db.Integer, db.ForeignKey("behaviors.behavior_id"))


class EmptyMedia(db.Model):
    __tablename__ = "empty_media"
    empty_medium_id = db.Column(db.String(22), primary_key=True)
    section = db.Column(db.Integer, db.ForeignKey("sections.section_id"))
    medium_datetime = db.Column(db.DateTime)
    path = db.Column(db.String(255))
    checked = db.Column(db.Boolean, default=False)


class DetectedMedia(db.Model):
    __tablename__ = "detected_media"
    detected_medium_id = db.Column(db.String(22), primary_key=True)
    section = db.Column(db.Integer, db.ForeignKey("sections.section_id"))
    medium_datetime = db.Column(db.DateTime)
    path = db.Column(db.String(255))
    reviewed = db.Column(db.Boolean, default=False)
    empty_checker = db.Column(db.Integer, db.ForeignKey("members.member_id"))


class Individuals(db.Model):
    __tablename__ = "individuals"
    individual_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    taxon_order_by_ai = db.Column(db.Integer, db.ForeignKey("species.taxon_order"))
    taxon_order_by_human = db.Column(db.Integer, db.ForeignKey("species.taxon_order"))
    medium = db.Column(db.String(22), db.ForeignKey("media.medium_id"))
    prey = db.Column(db.Boolean, default=False)
    prey_name = db.Column(db.String(15))
    tagged = db.Column(db.Boolean, default=False)
    ring_number = db.Column(db.String(15))
    file_type = db.Column(db.String(5))
    xmin = db.Column(db.Float)
    xmax = db.Column(db.Float)
    ymin = db.Column(db.Float)
    ymax = db.Column(db.Float)
    prey_identify_by = db.Column(db.Integer, db.ForeignKey("members.member_id"))


class DetectedIndividuals(db.Model):
    __tablename__ = "detected_individuals"
    pending_individual_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    taxon_order_by_ai = db.Column(db.Integer, db.ForeignKey("species.taxon_order"))
    medium = db.Column(
        db.String(22), db.ForeignKey("detected_media.detected_medium_id")
    )
    xmin = db.Column(db.Float)
    xmax = db.Column(db.Float)
    ymin = db.Column(db.Float)
    ymax = db.Column(db.Float)


class Members(db.Model):
    __tablename__ = "members"
    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(5))
    last_name = db.Column(db.String(5))
    position = db.Column(db.Integer, db.ForeignKey("positions.position_id"))
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)


class Contributions(db.Model):
    __tablename__ = "contributions"
    contribution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contributor = db.Column(db.Integer, db.ForeignKey("members.member_id"))
    num_files = db.Column(db.Integer, nullable=False)
    action = db.Column(db.Integer, db.ForeignKey("actions.action_id"))
    time = db.Column(db.DateTime, default=datetime.utcnow)


class Species(db.Model):
    __tablename__ = "species"
    taxon_order = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.String(100))
    english_common_name = db.Column(db.String(100))
    chinese_common_name = db.Column(db.String(50))
    category = db.Column(db.String(15))
    order = db.Column(db.String(50))
    family_name = db.Column(db.String(50))
    family_latin_name = db.Column(db.String(50))
    taiwan_status = db.Column(db.String(50))
    matzu_status = db.Column(db.String(50))
    kinmen_status = db.Column(db.String(50))
    pratas_status = db.Column(db.String(50))
    endemism = db.Column(db.String(50))
    conservation_status = db.Column(db.String(5))
    usage_count = db.Column(db.Integer, default=0)


class SpeciesCodes(db.Model):
    __tablename__ = "species_codes"
    taxon_order = db.Column(
        db.Integer, db.ForeignKey("species.taxon_order"), primary_key=True
    )
    code = db.Column(db.String(10), primary_key=True)


class Behaviors(db.Model):
    __tablename__ = "behaviors"
    behavior_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chinese_name = db.Column(db.String(20), nullable=False)


class Positions(db.Model):
    __tablename__ = "positions"
    position_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))


class MountTypes(db.Model):
    __tablename__ = "mount_types"
    mount_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15))


class Cameras(db.Model):
    __tablename__ = "cameras"
    camera_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(10))


class Habitats(db.Model):
    __tablename__ = "habitats"
    habitat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chinese_name = db.Column(db.String(10))
    english_name = db.Column(db.String(25))


class Projects(db.Model):
    __tablename__ = "projects"
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15))


class Layers(db.Model):
    __tablename__ = "layers"
    layer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15))


class Events(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chinese_name = db.Column(db.String(15))
    english_name = db.Column(db.String(15))


class Actions(db.Model):
    __tablename__ = "actions"
    action_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15))


class UpdateInfo(db.Model):
    __tablename__ = "update_info"
    update_info_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_file_name = db.Column(db.String(30))
    detail_file_name = db.Column(db.String(30))
    create_date = db.Column(db.Date, default=datetime.today)
    checked = db.Column(db.Boolean, default=False)
