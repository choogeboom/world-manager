import enum
from typing import Optional

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from utils.sql import AwareDateTime, tz_aware_now, ResourceMixin

from world_manager.extensions import db


class UserRole(enum.Enum):
    admin = 1
    member = 2


class User(ResourceMixin, db.Model):

    id = db.Column(db.BigInteger,
                   primary_key=True)

    # Authentication
    role = db.Column(db.Enum(UserRole,
                             native_enum=False, name='user_role_type'),
                     index=True,
                     nullable=False,
                     server_default='member')
    is_active = db.Column(db.Boolean(),
                          nullable=False,
                          server_default='1')

    username = db.Column(db.String(24),
                         nullable=False,
                         unique=True,
                         index=True)
    email_address = db.Column(db.String(255),
                              nullable=False,
                              unique=True,
                              index=True)
    password = db.Column(db.String(128), nullable=False, server_default='')

    # Activity Tracking
    login_count = db.Column(db.Integer, nullable=False, default=0)
    current_login_time = db.Column(AwareDateTime())
    current_login_ip_address = db.Column(db.String(45))
    last_login_time = db.Column(AwareDateTime())
    last_login_ip_address = db.Column(db.String(45))

    def __init__(self, **kwargs):
        super.__init__(**kwargs)
        self.password = User.encrypt_password(kwargs.get('password', ''))

    @staticmethod
    def find_by_identity(identity: str) -> 'User':
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return User.query.filter(
            (User.email_address == identity)
            | (User.username == identity)).first()

    @staticmethod
    def encrypt_password(plaintext_password: str) -> Optional[str]:
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)
        return None

    @staticmethod
    def deserialize_token(token: str) -> Optional['User']:
        """
        Obtain a user from de-serializing a signed token.

        :param token: Signed token.
        :type token: str
        :return: User instance or None
        """
        private_key = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'])
        try:
            decoded_payload = private_key.loads(token)

            return User.find_by_identity(decoded_payload.get('user_email'))
        except Exception:
            return None

    def authenticate(self, password: str='') -> bool:
        """
        Ensure a user is authenticated, and optionally check their password.

        :param password: Optionally verify this as their password
        """
        if password:
            return check_password_hash(self.password, password)

        return True

    def register_login(self, ip_address):
        self.sign_in_count += 1

        self.last_login_ip_address = self.current_login_ip_address
        self.last_login_time = self.current_login_time

        self.current_login_ip_address = ip_address
        self.current_login_time = tz_aware_now()

        return self.save()




