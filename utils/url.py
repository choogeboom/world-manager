from urllib.parse import urljoin

from flask import request


def get_safe_next_url(target: str) -> str:
    """
    Ensure a relative URL path is on the same domain as this host.
    This protects against the 'Open redirect vulnerability'.

    :param target: Relative url (typically supplied by Flask-Login)
    :return: str
    """
    return urljoin(request.host_url, target)
