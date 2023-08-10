from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, InputRequired


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
