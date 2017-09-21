from typing import Optional

from flask import Flask

from world_manager.extensions import db, debug_toolbar

from world_manager.blueprints.page.views import page


ACTIVE_EXTENSIONS = [db, debug_toolbar]
ACTIVE_BLUEPRINTS = [page]


def create_app(settings_override: Optional[dict]=None) -> Flask:
    """
    Create a Flask app

    :param settings_override: any settings to override
    :return: flask app
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)
    configure_logging(app)

    initialize_extensions(app)
    register_blueprints(app)

    return app


def initialize_extensions(app: Flask) -> None:
    """
    Initialize extensions

    :param app: The flask app
    """
    for extension in ACTIVE_EXTENSIONS:
        extension.init_app(app)


def register_blueprints(app: Flask) -> None:
    """
    Register blueprints

    :param app: the flask app
    """
    for blueprint in ACTIVE_BLUEPRINTS:
        app.register_blueprint(blueprint)


def configure_logging(app: Flask) -> None:
    pass
