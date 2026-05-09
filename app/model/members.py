import uuid
import re
import sqlalchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy_serializer import SerializerMixin

import app.extensions as extensions
from app.model import enums


class ColumnSize:
    OIDC_SUB = 255
    PROFILE_PICTURE_URL = 255
    USER_NAME = 50
    DISPLAY_NAME = 50
    FIRST_NAME = 50
    LAST_NAME = 50


class Members(extensions.db.Model, SerializerMixin):
    __tablename__ = "members"
    id = extensions.db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    oidc_sub = extensions.db.Column(sqlalchemy.String(ColumnSize.OIDC_SUB), unique=True)
    profile_picture_url = extensions.db.Column(
        sqlalchemy.String(ColumnSize.PROFILE_PICTURE_URL)
    )
    gmail = extensions.db.Column(postgresql.CITEXT, nullable=False, unique=True)
    display_name = extensions.db.Column(sqlalchemy.String(ColumnSize.DISPLAY_NAME))
    user_name = extensions.db.Column(
        sqlalchemy.String(ColumnSize.USER_NAME),
    )
    first_name = extensions.db.Column(
        sqlalchemy.String(ColumnSize.FIRST_NAME),
        nullable=False,
    )
    last_name = extensions.db.Column(
        sqlalchemy.String(ColumnSize.LAST_NAME),
        nullable=False,
    )
    position = extensions.db.Column(sqlalchemy.Enum(enums.Positions))
    is_admin = extensions.db.Column(
        sqlalchemy.Boolean,
        default=False,
        server_default=sqlalchemy.text("FALSE"),
        nullable=False,
    )
    is_super_admin = extensions.db.Column(
        sqlalchemy.Boolean,
        default=False,
        server_default=sqlalchemy.text("FALSE"),
        nullable=False,
    )
    blocked = extensions.db.Column(
        sqlalchemy.Boolean,
        default=False,
        server_default=sqlalchemy.text("FALSE"),
        nullable=False,
    )
    activated = extensions.db.Column(
        sqlalchemy.Boolean,
        default=False,
        server_default=sqlalchemy.text("FALSE"),
        nullable=False,
    )

    @sqlalchemy.orm.validates("gamil")
    def validate_email(self, key, email):

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email
