from utils.sql import tz_aware_now


def current_year() -> int:
    """
    Return the current year
    :return: the current year
    """
    return tz_aware_now().year


def ability_score(ability: dict):
    other_bonuses = (v for d, v in ability['score']['other'])
    return ability['score']['base'] + ability['score']['racial'] \
        + sum(other_bonuses)


def ability_modifier(ability: dict):
    score = ability_score(ability)
    return (score - 10) // 2


def saving_throw_modifier(ability: dict, proficiency_bonus: int):
    proficiency = ability['saving_throws']['proficient']*proficiency_bonus
    other_bonuses = (v for d, v in ability['saving_throws']['other'])
    return ability_modifier(ability) + proficiency + sum(other_bonuses)


def skill_modifier(ability: dict, skill, proficiency_bonus):
    proficiency = ability['skills'][skill]['proficient']*proficiency_bonus
    other_bonuses = (v for d, v in ability['skills'][skill]['other'])
    return ability_modifier(ability) + proficiency + sum(other_bonuses)


def format_other_bonuses(other):
    return ', '.join(f'{d}: {v:+d}' for d, v in other)
