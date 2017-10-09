from utils.sql import tz_aware_now


def current_year() -> int:
    """
    Return the current year
    :return: the current year
    """
    return tz_aware_now().year
