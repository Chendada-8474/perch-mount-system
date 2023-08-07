import os
import sys
from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import (
    StringField,
    DateField,
    SubmitField,
    SelectField,
    EmailField,
    FloatField,
    SelectMultipleField,
    TextAreaField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
)

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


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
