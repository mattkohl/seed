from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool

from config import config


db = SQLAlchemy(engine_options={"poolclass": NullPool})


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    from src.ui import ui as ui_blueprint
    app.register_blueprint(ui_blueprint)

    from src.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
