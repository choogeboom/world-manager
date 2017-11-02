import click

from sqlalchemy_utils import database_exists, create_database

from utils.sql import ScopedSession
from world_manager.app import create_app
from world_manager.extensions import db


# Create an app context for the database connection.
from world_manager.model import stat

app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@cli.command()
@click.option('--with-test-db/--no-with-test-db', default=False,
              help='Create a test db too?')
def init(with_test_db):
    """
    Initialize the database.

    :param with_test_db: Create a test database
    :return: None
    """
    db.drop_all()
    db.create_all()

    if with_test_db:
        db_uri = '{0}_test'.format(app.config['SQLALCHEMY_DATABASE_URI'])

        if not database_exists(db_uri):
            create_database(db_uri)

    return None


# noinspection PyArgumentList
@cli.command()
def seed():
    """
    Seed the database with an initial user.
    """
    schools_of_magic = ('Abjuration', 'Divination', 'Enchantment', 'Evocation',
                        'Illusion', 'Necromancy', 'Transmutation')
    with ScopedSession() as session:
        for school_name in schools_of_magic:
            session.add(stat.SchoolOfMagic(name=school_name))


@cli.command()
@click.option('--with-test-db/--no-with-test-db', default=False,
              help='Create a test db too?')
@click.pass_context
def reset(ctx, with_test_db):
    """
    Init and seed automatically.

    :param with_test_db: Create a test database
    :return: None
    """
    ctx.invoke(init, with_test_db=with_test_db)
    ctx.invoke(seed)

    return None

