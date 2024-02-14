import flask
import flask_jwt_extended

import resources
from routes import routing
import service
from src import model
from src import config
from src import app
import login
import login.app
import species_trie.app


app.app.config["SQLALCHEMY_DATABASE_URI"] = service.SQLALCHEMY_DATABASE_URI
app.app.config["SECRET_KEY"] = config.get_file_content(config.EnvKeys.FLASK_SECRET)
app.app.config["JWT_SECRET_KEY"] = config.get_file_content(config.EnvKeys.JWT_SECRET)
app.app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.get_jwt_access_token_expires()


resources.api.init_resources(routing.ROUTES)
resources.api.init_app(app.app)
login.jwt.init_app(app.app)
model.db.init_app(app.app)
model.migrate.init_app(app.app, model.db)


@app.app.route("/test", methods=["GET"])
@flask_jwt_extended.jwt_required()
def test():
    current_user = flask_jwt_extended.get_jwt_identity()
    claims = flask_jwt_extended.get_jwt()
    return flask.jsonify({"user": current_user, "claims": claims})


if __name__ == "__main__":
    app.app.run(host="127.0.0.1", debug=True)
