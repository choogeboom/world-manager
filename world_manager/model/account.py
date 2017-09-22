import enum

from world_manager.extensions import db


class UserRole(enum.Enum):
    admin = 1
    member = 2


class User(db.Model):

    id = db.Column(db.BigInteger,
                   primary_key=True)
    is_active = db.Column(db.Boolean(),
                          nullable=False,
                          server_default='1')
    role = db.Column(db.Enum(UserRole,
                             native_enum=False, name='user_role_type'),
                     index=True,
                     nullable=False,
                     server_default='member')

    username = db.Column(db.String(24),
                         nullable=False,
                         unique=True,
                         index=True)
    email_address = db.Column(db.String(255),
                              nullable=False,
                              unique=True,
                              index=True)
