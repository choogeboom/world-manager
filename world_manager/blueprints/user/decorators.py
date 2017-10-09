from functools import wraps

from flask import redirect
from flask_login import current_user


def anonymous_required(url: str='/settings'):
    """
    Redirect a user to a specific page if they are already signed in

    :param url:
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
