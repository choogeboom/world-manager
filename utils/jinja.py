from utils.sql import tz_aware_now


def current_year():
    """
    Returns the current year
    :return:
    """
    return tz_aware_now().year