import pytest

from config import settings
from world_manager.app import create_app
from world_manager.extensions import db as _db


@pytest.fixture(scope='session')
def app():
    db_uri = f'{settings.SQLALCHEMY_DATABASE_URI}_test'
    params = {
        'DEBUG': False,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': db_uri
    }

    _app = create_app(settings_override=params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


# noinspection PyShadowingNames
@pytest.fixture(scope='session')
def db(app):
    _db.drop_all(app=app)
    _db.create_all(app=app)

    return _db
