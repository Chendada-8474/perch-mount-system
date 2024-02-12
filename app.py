from flask import Flask

from routes import route_helper
from routes import routing
import service
from src import model
from src import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get_file(config.EnvKeys.FLASK_SECRET)
app.config["SQLALCHEMY_DATABASE_URI"] = service.SQLALCHEMY_DATABASE_URI

api = route_helper.PerchMountApi(app)
api.init_resources(routing.ROUTES)

model.db.init_app(app)
model.migrate.init_app(app, model.db)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
