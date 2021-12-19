"""Useful OSRS Metrics Constants."""
from typing import List

HISCORES_RESPONSE_SKILLS: List[str] = [
    "Overall",
    "Attack",
    "Defence",
    "Strength",
    "Hitpoints",
    "Ranged",
    "Prayer",
    "Magic",
    "Cooking",
    "Woodcutting",
    "Fletching",
    "Fishing",
    "Firemaking",
    "Crafting",
    "Smithing",
    "Mining",
    "Herblore",
    "Agility",
    "Thieving",
    "Slayer",
    "Farming",
    "Runecrafting",
    "Hunter",
    "Construction",
]

# Reformatted to valid MySQL columns:
# https://dev.mysql.com/doc/refman/8.0/en/identifiers.html
HISCORES_RESPONSE_ACTIVITIES: List[str] = [
    "LeaguePoints",
    "BountyHunter_Hunter",
    "BountyHunter_Rogue",
    "ClueScrolls_all",
    "ClueScrolls_beginner",
    "ClueScrolls_easy",
    "ClueScrolls_medium",
    "ClueScrolls_hard",
    "ClueScrolls_elite",
    "ClueScrolls_master",
    "LMS_Rank",
    "SoulWars_Zeal",
    "AbyssalSire",
    "AlchemicalHydra",
    "BarrowsChests",
    "Bryophyta",
    "Callisto",
    "Cerberus",
    "ChambersofXeric",
    "ChambersofXeric_ChallengeMode",
    "ChaosElemental",
    "ChaosFanatic",
    "CommanderZilyana",
    "CorporealBeast",
    "CrazyArchaeologist",
    "DagannothPrime",
    "DagannothRex",
    "DagannothSupreme",
    "DerangedArchaeologist",
    "GeneralGraardor",
    "GiantMole",
    "GrotesqueGuardians",
    "Hespori",
    "KalphiteQueen",
    "KingBlackDragon",
    "Kraken",
    "KreeArra",
    "KrilTsutsaroth",
    "Mimic",
    "Nightmare",
    "PhosanisNightmare",
    "Obor",
    "Sarachnis",
    "Scorpia",
    "Skotizo",
    "Tempoross",
    "TheGauntlet",
    "TheCorruptedGauntlet",
    "TheatreofBlood",
    "TheatreofBlood_HardMode",
    "ThermonuclearSmokeDevil",
    "TzKalZuk",
    "TzTokJad",
    "Venenatis",
    "Vettion",
    "Vorkath",
    "Wintertodt",
    "Zalcano",
    "Zulrah",
]

HISCORES_RESPONSE_ROWS: List[str] = (
    HISCORES_RESPONSE_SKILLS + HISCORES_RESPONSE_ACTIVITIES
)
HISCORES_RESPONSE_SKILL_COLS: List[str] = ["rnk", "lvl", "xp"]
HISCORE_RESPONSE_ACTIVITY_COLS: List[str] = ["rnk", "kc"]
"""
Unfortunately, `RANK`, `LEVEL`, and `COUNT` are all reserved words in DynamoDB:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html
"""
