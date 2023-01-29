"""Data model for quest guide."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from attrs import define, field
from get_and_parse_hiscores.lib.quest_guide.skill_util import (
    LEVEL_XP_BOUNDS,
    MIN_XP_PER_LEVEL,
    Skill,
    get_level_from_xp,
    str_to_skill,
)


class QuestReward(ABC):
    """Reward for completing a Quest."""

    @abstractmethod
    def helps_toward(self, requirement: QuestRequirement):
        """Whether this reward will help towards a later requirement."""


@define
class XPReward(QuestReward):
    """XP Granted for completing a quest."""

    skill: Skill = field(converter=str_to_skill)
    """Skill for the reward XP."""

    amount: int = field(converter=int)
    """Amount of XP granted."""

    def helps_toward(self, requirement: QuestRequirement):
        """Whether this XPReward helps toward a QuestRequirement."""
        if isinstance(requirement, SkillLevel):
            return requirement.skill == self.skill
        elif isinstance(requirement, Quest):
            return any(self.helps_toward(req) for req in requirement.requirements)
        else:  # pragma: no cover
            return False


class QuestRequirement(ABC):
    """Requirement for completing a Quest."""

    @abstractmethod
    def met_by(self, player: Player) -> bool:
        """Whether a Player satisfies this requirement."""


@define
class SkillLevel(QuestRequirement):
    """Level in a Skill."""

    skill: Skill = field(converter=str_to_skill)
    """Skill of this requirement."""

    level: int = field(default=None, converter=lambda x: int(x) if x is not None else x)
    """Level of this requirement."""

    xp: int = field(default=None, converter=lambda x: int(x) if x is not None else x)
    """XP of this requirement."""

    def __attrs_post_init__(self):
        """Require level or value."""
        if self.level is None and self.xp is None:
            raise TypeError(
                f"{type(self).__name__}.__init__() "
                "requires 1 of 2 keyword-only arguments: 'level' or 'xp'"
            )

        if self.level is None:
            self.level = get_level_from_xp(self.xp)
        if self.xp is None:
            self.xp = MIN_XP_PER_LEVEL[self.level]

        if self.level != get_level_from_xp(self.xp):
            lower, upper = LEVEL_XP_BOUNDS[self.level]
            raise ValueError(
                f"Invalid xp ({self.xp}) for level ({self.level}). Acceptable range "
                f"is [{lower}, {upper})"
            )

    def met_by(self, player: Player) -> bool:
        """Whether a Player satisfies this skill requirement."""
        for level in player.skill_levels:
            if level.skill == self.skill and level.xp >= self.xp:
                return True
        else:
            return False


@define
class Quest(QuestRequirement):
    """A Quest."""

    name: str = field()
    """Name of this quest."""

    requirements: List[QuestRequirement] = field(factory=list)
    """Requirements for completing this quest."""

    rewards: List[QuestReward] = field(factory=list)
    """Rewards this quest grants on completion."""

    def met_by(self, player: Player) -> bool:
        """Whether a Player meets the requirements for this Quest."""
        for requirement in self.requirements:
            if isinstance(requirement, SkillLevel) and not requirement.met_by(player):
                return False
            elif (
                isinstance(requirement, Quest)
                and requirement not in player.completed_quests
            ):
                return False
        else:
            return True


@define
class Player(object):
    """A Player"""

    name: str = field()
    """Name of this player."""

    skill_levels: List[SkillLevel] = field(factory=list)
    """Player's current levels."""

    completed_quests: List[Quest] = field(factory=list)
    """Quests the player has completed."""
