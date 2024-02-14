import flask
import service
from src import config

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = service.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.get_file_content(config.EnvKeys.FLASK_SECRET)
