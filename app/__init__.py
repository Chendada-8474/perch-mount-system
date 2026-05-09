from flask import Flask
import flask_cors

from app import model
from app.extensions import db, migrate, jwt
from app.error_handler import blueprint as error_handler_blueprint
from app.auth import blueprint as login_blueprint
from app.taxa import blueprint as taxa_blueprint
from app.resources.perchai import blueprint as perchai_blueprint
from app.resources.data_export import blueprint as data_export_blueprint
from app.resources.features import blueprint as features_blueprint


def create_app(config_object="config.Config") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    flask_cors.CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(perchai_blueprint, url_prefix="/api/perchai")
    app.register_blueprint(data_export_blueprint, url_prefix="/api/data")
    app.register_blueprint(taxa_blueprint, url_prefix="/api/taxa")
    app.register_blueprint(error_handler_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(features_blueprint, url_prefix="/api/features")

    return app
