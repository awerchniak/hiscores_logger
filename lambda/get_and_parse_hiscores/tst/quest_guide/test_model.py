import get_and_parse_hiscores.lib.quest_guide.model as model
import pytest


@pytest.mark.parametrize(
    "xp,expected_level",
    [(1e6, 73), (1e8, 99)],
)
def test_init_skill_level_from_xp(xp, expected_level):
    assert expected_level == model.SkillLevel("crafting", xp=xp).level


def test_init_skill_level_invalid_skill():
    with pytest.raises(KeyError):
        model.SkillLevel("invalid")


def test_init_skill_level_missing_fields():
    with pytest.raises(TypeError):
        model.SkillLevel("crafting")


def test_init_skill_level_invalid():
    with pytest.raises(ValueError):
        s1 = model.SkillLevel("crafting", level=80, xp=1e6)


def test_met_by_no_requirements():
    q1 = model.Quest("q1")
    p1 = model.Player("p1")
    assert q1.met_by(p1)


def test_met_by_requirements():
    q1 = model.Quest("q1")
    s1 = model.SkillLevel("slayer", level=20)
    r1 = model.XPReward("crafting", 1e4)
    q2 = model.Quest("q2", [q1, s1], rewards=[r1])
    p2 = model.Player("p2", [s1], [q1])
    assert s1.met_by(p2)
    assert q2.met_by(p2)


def test_not_met_by_quest_requirements():
    q1 = model.Quest("q1")
    p1 = model.Player("p1")
    q2 = model.Quest("q2", [q1])
    assert not q2.met_by(p1)


def test_not_met_by_skill_requirement():
    s1 = model.SkillLevel("slayer", level=20)
    q1 = model.Quest("q1", [s1])
    p1 = model.Player("p1", skill_levels=[model.SkillLevel("slayer", level=10)])
    assert not q1.met_by(p1)


def test_helps_toward_skill_requirement():
    reward = model.XPReward("slayer", 1e4)
    requirement = model.SkillLevel("slayer", 20)
    assert reward.helps_toward(requirement)


def test_does_not_help_toward_skill_requirement():
    reward = model.XPReward("slayer", 1e4)
    requirement = model.SkillLevel("crafting", 20)
    assert not reward.helps_toward(requirement)


def test_helps_toward_quest_requirement():
    reward = model.XPReward("slayer", 1e4)
    quest = model.Quest("quest", [model.SkillLevel("slayer", 20)])
    assert reward.helps_toward(quest)


def test_does_not_help_toward_quest_requirement():
    reward = model.XPReward("slayer", 1e4)
    quest = model.Quest("quest")
    assert not reward.helps_toward(quest)
