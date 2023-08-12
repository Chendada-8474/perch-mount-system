from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    SelectField,
    FloatField,
    IntegerField,
    DateField,
    BooleanField,
    SelectMultipleField,
)

from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired
from datetime import datetime


class NewPerchMount(FlaskForm):
    perch_mount_name = StringField("棲架名稱", validators=[DataRequired()])
    latitude = FloatField("緯度", validators=[InputRequired()])
    longitude = FloatField("經度", validators=[InputRequired()])
    habitat = SelectField("棲地類型", validators=[DataRequired()])
    project = SelectField("計畫", validators=[DataRequired()])
    layer = SelectField("分層")
    submit = SubmitField("新增")

    def init_choices(self, habitats=None, projects=None, layers=None):
        self.habitat.choices = habitats
        self.project.choices = projects
        self.layer.choices = layers


class NewMember(FlaskForm):
    user_name = StringField("使用者名稱", validators=[DataRequired()])
    phone_number = StringField("電話", validators=[DataRequired()])
    first_name = StringField("名字")
    last_name = StringField("姓氏")
    position = SelectField("職位")
    submit = SubmitField("新增")

    def init_choices(self, positions):
        self.position.choices = positions


class NewBehavior(FlaskForm):
    chinese_name = StringField("行為", validators=[DataRequired()])
    submit = SubmitField("新增")


class NewCamera(FlaskForm):
    model_name = StringField("型號", validators=[DataRequired()])
    submit = SubmitField("新增")


class NewEvent(FlaskForm):
    chinese_name = StringField("事件中文", validators=[DataRequired()])
    english_name = StringField("事件英文", validators=[DataRequired()])
    submit = SubmitField("新增")


class Parameter(FlaskForm):
    perch_mount_id = IntegerField("棲架編號", validators=[DataRequired()])
    project = StringField("計畫", validators=[DataRequired()])
    perch_mount_name = StringField("棲架名稱", validators=[DataRequired()])
    mount_type = SelectField("棲架類型", validators=[DataRequired()])
    camera = SelectField("相機", validators=[DataRequired()])
    start_time = DateTimeLocalField("開始時間")
    check_date = DateField(
        "回收日期",
        default=datetime.today,
        format="%Y-%m-%d",
        validators=[DataRequired()],
    )
    operators = SelectMultipleField("回收人員")
    valid = BooleanField("是否有效", default=True, validators=[DataRequired()])
    note = StringField("備註")
    submit = SubmitField("下載")

    def init_choice(self, mount_types, cameras, members):
        self.mount_type.choices = [(m["mount_type_id"], m["name"]) for m in mount_types]
        self.camera.choices = [(c["camera_id"], c["model_name"]) for c in cameras]
        self.operators.choices = [(m["member_id"], m["first_name"]) for m in members]
