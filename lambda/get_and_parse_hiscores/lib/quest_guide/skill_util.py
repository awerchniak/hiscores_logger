"""Utilies for working with OSRS Skills."""

from enum import Enum
from math import floor
from typing import List, Tuple, Union

from get_and_parse_hiscores.lib.hiscores.constants import HISCORES_RESPONSE_SKILLS


def _min_xp_for_level(max_level: int) -> List[int]:
    # https://oldschool.runescape.wiki/w/Experience
    points = 0
    result = [0]
    for lvl in range(1, max_level + 1):
        result.append(int(floor(points / 4)))
        points += floor(lvl + 300.0 * 2.0 ** (lvl / 7.0))
    return result


MAX_LEVEL: int = 99
"""Maximum level achievable in RuneScape."""

MIN_XP_PER_LEVEL: List[int] = _min_xp_for_level(MAX_LEVEL)
"""Minimum XP, indexed by level."""

LEVEL_XP_BOUNDS: List[Tuple[int]] = [
    (MIN_XP_PER_LEVEL[i], MIN_XP_PER_LEVEL[i + 1]) for i in range(MAX_LEVEL)
] + [(MIN_XP_PER_LEVEL[MAX_LEVEL], "inf")]
"""XP Bounds for each level."""


def get_level_from_xp(xp: int, min_level: int = 1, max_level: int = MAX_LEVEL) -> int:
    """Get a level from an amount of XP gained (binary search)."""
    if MIN_XP_PER_LEVEL[max_level] <= xp:
        return max_level

    if max_level - min_level <= 1:
        return min_level

    midpoint = int((max_level + min_level) / 2)
    if MIN_XP_PER_LEVEL[midpoint] > xp:
        return get_level_from_xp(xp, min_level, midpoint)

    return get_level_from_xp(xp, midpoint, max_level)


Skill = Enum("Skill", [x.upper() for x in HISCORES_RESPONSE_SKILLS])
"""Skills in RuneScape."""


def str_to_skill(skill: Union[Skill, str]) -> Skill:
    """Get a skill by name."""
    if isinstance(skill, Skill):  # pragma: no cover
        return skill
    elif isinstance(skill, str):
        try:
            return Skill[skill.upper()]
        except KeyError as e:
            raise KeyError(
                f"'{e}' is not a valid skill. Choose from: {Skill._member_names_}"
            )
