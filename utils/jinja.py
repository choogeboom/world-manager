from utils.sql import tz_aware_now


def current_year() -> int:
    """
    Return the current year
    :return: the current year
    """
    return tz_aware_now().year


def ability_score(ability: dict):
    return ability['score']['base'] + ability['score']['racial'] \
           + sum_other_bonuses(ability['score']['other'])


def ability_modifier(ability: dict):
    score = ability_score(ability)
    return (score - 10) // 2


def saving_throw_modifier(ability: dict, proficiency_bonus: int):
    proficiency = ability['saving_throws']['proficient']*proficiency_bonus
    return ability_modifier(ability) + proficiency \
           + sum_other_bonuses(ability['saving_throws']['other'])


def skill_modifier(ability: dict, skill, proficiency_bonus):
    proficiency = ability['skills'][skill]['proficient']*proficiency_bonus
    return ability_modifier(ability) + proficiency \
           + sum_other_bonuses(ability['skills'][skill]['other'])


def format_other_bonuses(other):
    return ', '.join(f'{d}: {v:+d}' for d, v in other)


def armor_score(armor):
    other_bonuses = (v for d, v in armor['other'])
    return armor['base'] + sum(other_bonuses)


def sum_other_bonuses(other):
    return sum(v for _, v in other)
