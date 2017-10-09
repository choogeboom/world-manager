from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_jsontools import JsonSerializableBase
from flask_sqlalchemy import SQLAlchemy, Model
from flask_jsglue import JSGlue
from flask_wtf import CSRFProtect

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declared_attr, DeclarativeMeta

from utils.string import to_snake_case


class ModelBase(Model, JsonSerializableBase):
    """
    Base class for all models.

    Makes it so that all models are JSON serializable, and supplies a
    """

    # noinspection PyMethodParameters
    @declared_attr
    def __tablename__(cls):
        """
        Automatically generates a __tablename__ for a mapped class to be the
        snake_case version of that class name. For example, the class `MyModel`
        would automatically have a __tablename__ value of 'my_model'
        :return:
        """
        return to_snake_case(cls.__name__)

    def __init__(self, **kwargs):
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)

    def __repr__(self: DeclarativeMeta):
        column_names = (c.name for c in self.__mapper__.columns)
        kwargs = ', '.join(f'{n}={getattr(self, n)!r}' for n in column_names)
        return f'{self.__class__.__name__}({kwargs})'

    def as_dict(self: DeclarativeMeta):
        column_names = (c.name for c in self.__mapper__.columns)
        return {n: getattr(self, n) for n in column_names}

    @property
    def session(self):
        instance_state = inspect(self)
        return instance_state.session or db.session


db = SQLAlchemy(model_class=ModelBase)
debug_toolbar = DebugToolbarExtension()
jsglue = JSGlue()
mail = Mail()
csrf = CSRFProtect()
