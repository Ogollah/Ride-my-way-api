# api/__init__.py
"""
    This module initialize the api.
"""
from flask_api import FlaskAPI

# local import
from instance.config import app_config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    return app