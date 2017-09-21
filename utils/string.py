import re


def to_camel_case(string: str, *, title_case: bool=False, delimiters=(' ', '_')):
    """
    Returns a camelCased version of a string
    :param string:
    :param title_case: Whether the output should have a first capital letter.
    :param delimiters: Word separators. These should be valid regex character
           classes.
    :return: a camel-cased string
    """
    delimiter_class = f"[{''.join(delimiters)}]"
    string_start = '^|' if title_case else ''
    delimiter_pattern = f"(?:{string_start}{delimiter_class})"
    pattern = f"{delimiter_pattern}+(\\w)"
    return re.sub(pattern, lambda mo: mo.group(1).upper(), string)


def to_snake_case(string: str) -> str:
    """
    Converts a string to snake_case
    :param string:
    :return:
    """
    # First replace all white space with _
    string = re.sub(r'_*\W+_*', '_', string.strip())
    string = re.sub(r'([A-Z])([A-Z]+)(?=[A-Z]|_|$)',
                    lambda mo: mo[1] + mo[2].lower(),
                    string)
    string = re.sub(r'([a-z])([A-Z])',
                    r'\1_\2',
                    string)
    string = re.sub(r'\A_+|_+\Z', '', string)  # remove leading and trailing _
    return string.lower()


def is_number(s: str) -> bool:
    """
    Return True if the string can be converted to a float
    :param s:
    :return:
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_integer(s: str) -> bool:
    """
    Return True if the string can be converted to an integer
    :param s: the string
    :return:
    """
    try:
        int(s)
        return True
    except ValueError:
        return False
