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
    damage_types = ('Acid', 'Bludgeoning', 'Cold', 'Fire', 'Force', 'Lightning',
                    'Necrotic', 'Piercing', 'Poison', 'Psychic', 'Radiant',
                    'Slashing', 'Thunder')
    coin_types = (
        ('Copper', 'cp', 1),
        ('Silver', 'sp', 10),
        ('Electrum', 'ep', 50),
        ('Gold', 'gp', 100),
        ('Platinum', 'pp', 1000)
    )
    abilities = (
        ('Strength', 'STR'),
        ('Dexterity', 'DEX'),
        ('Constitution', 'CON'),
        ('Intelligence', 'INT'),
        ('Wisdom', 'WIS'),
        ('Charisma', 'CHA')
    )
    skills = (
        ('Athletics', 'STR'),
        ('Acrobatics', 'DEX'),
        ('Sleight of Hand', 'DEX'),
        ('Stealth', 'DEX'),
        ('Arcana', 'INT'),
        ('History', 'INT'),
        ('Investigation', 'INT'),
        ('Nature', 'INT'),
        ('Religion', 'INT'),
        ('Animal Handling', 'WIS'),
        ('Insight', 'WIS'),
        ('Medicine', 'WIS'),
        ('Perception', 'WIS'),
        ('Survival', 'WIS'),
        ('Deception', 'CHA'),
        ('Intimidation', 'CHA'),
        ('Performance', 'CHA'),
        ('Persuasion', 'CHA')
    )
    with ScopedSession() as session:
        for school_name in schools_of_magic:
            session.add(stat.SchoolOfMagic(name=school_name))
        session.commit()
        for damage_type_name in damage_types:
            session.add(stat.DamageType(name=damage_type_name))
        session.commit()
        for name, abbreviation, value in coin_types:
            session.add(stat.CoinType(name=name, abbreviation=abbreviation,
                                      value=value))
        session.commit()
        for name, abbreviation in abilities:
            session.add(stat.Ability(name=name, abbreviation=abbreviation))
        session.commit()
        for name, default_ability in skills:
            ability = session.query(stat.Ability).filter_by(
                abbreviation=default_ability).one()
            session.add(stat.Skill(name=name, default_ability_id=ability.id))


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

