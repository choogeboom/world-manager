import datetime
from typing import Optional

import pytz
from sqlalchemy.types import TypeDecorator, DateTime

from world_manager.extensions import db


def tz_aware_now():
    """
    Return a timezone aware Now
    :return: datetime
    """
    return datetime.datetime.now(pytz.utc)


class AwareDateTime(TypeDecorator):
    """
    A DateTime which can only store time-zone aware datetimes

    Source:
      https://gist.github.com/inklesspen/90b554c864b99340747e
    """

    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime.datetime):
            if value.tzinfo is None:
                raise ValueError('{!r} must be TZ-aware!'.format(value))
        return value

    def __repr__(self):
        return 'AwareDateTime()'


class ResourceMixin:
    """
    Adds date created and date updated columns to the sources
    """
    db_created_on = db.Column(
        AwareDateTime(),
        default=tz_aware_now,
    )
    db_updated_on = db.Column(
        AwareDateTime(),
        default=tz_aware_now,
    )

    def __setattr__(self, key, value):
        if hasattr(self, key):
            if getattr(self, key) != value:
                super().__setattr__(key, value)
                super().__setattr__('db_updated_on', tz_aware_now())
        else:
            super().__setattr__(key, value)

    def save(self):
        """
        Save a model instance

        :return: model instance
        """
        db.session.add(self)
        db.session.flush()
        db.session.commit()

        return self

    def delete(self):
        """
        Delete a model instance

        :return: the result of the commit
        """
        db.session.delete(self)
        return db.session.commit()

    def __str__(self):
        """
        create a human readable version of the class instance

        :return: string
        """
        obj_id = hex(id(self))
        if hasattr(self, '__table__'):
            columns = self.__table__.c.keys()
        else:
            columns = []
        values = ', '.join('{!s}={!r}'.format(n, getattr(self, n))
                           for n in columns)
        return '<{!s} {!s}({!s})>'.format(obj_id,
                                          self.__class__.__name__,
                                          values)


def execute_script(path, engine):
    with open(path, 'r') as f:
        for command in split_commands(f):
            engine.execute(command)


def split_commands(lines):
    no_comments = ''.join(strip_comments(lines))
    return no_comments.split(';')


def strip_comments(lines):
    return filter(lambda x: not x.startswith('--') and x.strip('\n'),
                  lines)


class ScopedSession:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.session: Optional[db.Session] = None

    def __enter__(self) -> db.Session:
        self.session = db.create_scoped_session(*self.args,
                                                **self.kwargs)
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if self.session:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()

            self.session.close()

