from world_manager.extensions import db


ACTIVE_EXTENSIONS = [db]


def create_app(settings_override: dict=None):
    """
    Create a Flask app

    :param settings_override: any settings to override
    :return: flask app
    """