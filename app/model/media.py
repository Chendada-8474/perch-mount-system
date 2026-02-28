import uuid
import sqlalchemy
from sqlalchemy.dialects import postgresql
import sqlalchemy.orm
from sqlalchemy_serializer import SerializerMixin

from app import extensions
from app.model import enums
from app.model import fk_names


class Media(extensions.db.Model, SerializerMixin):
    __tablename__ = "media"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    section_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.SECTIONS_ID),
        nullable=False,
    )
    medium_datetime = extensions.db.Column(sqlalchemy.DateTime)
    created_at = extensions.db.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
        server_default=sqlalchemy.func.now(),
        nullable=False,
    )
    medium_type = extensions.db.Column(
        sqlalchemy.Enum(enums.MediaTypes), nullable=False
    )
    nas_path = extensions.db.Column(sqlalchemy.String(255))
    s3_file_name = extensions.db.Column(sqlalchemy.String(255))
    status = extensions.db.Column(
        sqlalchemy.Enum(enums.MediaStatus),
        default="UNDETECTED",
        server_default="UNDETECTED",
    )
    individuals = sqlalchemy.orm.relationship("Individuals", lazy="selectin")
    # section = sqlalchemy.orm.relationship("Sections", lazy="joined")
    unchecked_contents = sqlalchemy.orm.relationship(
        "UncheckedMediaContents", uselist=False, lazy="selectin"
    )
    detected_contents = sqlalchemy.orm.relationship(
        "MediaDetectedContents", uselist=False, lazy="selectin"
    )
    checked_contents = sqlalchemy.orm.relationship(
        "MediaCheckedContents", uselist=False, lazy="selectin"
    )
    unreviewued_contents = sqlalchemy.orm.relationship(
        "UnreviewedMediaContents", uselist=False, lazy="selectin"
    )
    reviewed_contents = sqlalchemy.orm.relationship(
        "ReviewedMediaContents", uselist=False, lazy="selectin"
    )


class UndetectedMediaContents(extensions.db.Model, SerializerMixin):
    __tablename__ = "undetected_media_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
        primary_key=True,
    )


class MediaDetectedContents(extensions.db.Model, SerializerMixin):
    __tablename__ = "media_detected_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
        primary_key=True,
    )
    detected_at = extensions.db.Column(sqlalchemy.DateTime)


class MediaCheckedContents(extensions.db.Model, SerializerMixin):
    __tablename__ = "media_checked_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
        primary_key=True,
    )

    empty_checked_at = extensions.db.Column(sqlalchemy.DateTime)
    empty_checker_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
    )


class UncheckedMediaContents(extensions.db.Model, SerializerMixin):
    __tablename__ = "unchecked_media_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
        primary_key=True,
    )


class UnreviewedMediaContents(extensions.db.Model, SerializerMixin):
    __tablename__ = "unreviewed_media_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
        primary_key=True,
    )


class ReviewedMediaContents(extensions.db.Model, SerializerMixin):
    __tablename__ = "reviewed_media_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
        primary_key=True,
    )
    reviewed_at = extensions.db.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.sql.func.now(),
        nullable=False,
    )
    reviewer_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
        nullable=False,
    )
    featured_by_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEMBERS_ID),
    )
    event_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.EVENTS_ID),
    )
    behavior_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.BEHAVIORS_ID),
    )
    behavior = sqlalchemy.orm.relationship("Behaviors", lazy="selectin")
    event = sqlalchemy.orm.relationship("Events", lazy="selectin")


class AccidentalMediaContents(extensions.db.Model, SerializerMixin):
    __tablename__ = "accidental_media_contents"
    medium_id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(fk_names.MEDIA_ID),
        nullable=False,
        primary_key=True,
    )
