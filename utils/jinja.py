from utils.sql import tz_aware_now


def current_year() -> int:
    """
    Return the current year
    :return: the current year
    """
    return tz_aware_now().year


def ability_modifier(ability: dict):
    return ability['score']['base'] + ability['score']['racial'] \
           + sum(ability['score']['other'])


def saving_throw_modifier(ability: dict, proficiency_bonus: int):
    return ability_modifier(ability) \
           + ability['saving_throws']['proficient']*proficiency_bonus \
           + sum(ability['saving_throws'])


def skill_modifier(ability: dict, skill, proficiency_bonus):
    return ability_modifier(ability) \
           + ability['skills'][skill]['proficient']*proficiency_bonus \
           + sum(ability['skills'][skill]['other'])
