#!/.venv/bin/python
"""Python script to migrate RDS HiScores database to DDB."""
import logging
import requests


from collections import OrderedDict
from datetime import datetime, timedelta
from functools import reduce
from typing import List

logging.basicConfig(level=logging.INFO)

PLAYERS = ["ElderPlinius", "Tarvis Devor", "Brec", "Dethaele"]
TABLE_START_END = ["2020-08-14", "2022-01-02"]
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
HISCORES_RESPONSE_SKILL_COLS: List[str] = ["rank", "level", "experience"]
TABLE_MAP: dict = {"rank": "rnk", "level": "lvl", "experience": "xp"}
API = "https://ti2bowg785.execute-api.us-east-1.amazonaws.com/default/QueryOsrsMetricsDbLambda"

def build_sql(table: str, skills: List[str], player: str, boundaries: List[str]):
    """Build MySQL Statement for querying HiScores DB."""
    return (
        f"SELECT timestamp,{','.join(skills)} FROM {table} "
        f"WHERE player='{player}' AND timestamp > '{boundaries[0]}' "
        f"AND timestamp < '{boundaries[1]}' ORDER BY timestamp ASC"
    )


def parse_response_item(response_item: List, table: str, skills: List[str], player: str):
    """Parse data returned by HiScores DB.

    Examples:
    >>> response_item = ['2021-12-23 14:55:43', 52297822, 3274504, 2054713, 5403638]
    >>> parse_response(response_item, "skills.experience", ["Overall", "Attack", "Defence", "Strength"], "ElderPlinius")
    {'timestamp':'2021-12-23 14:55:43', 'player': 'ElderPlinius',' Overall': 52297822, 'Attack': 3274504, 'Defence': 2054713, 'Strength': 5403638}

    """

    result = dict()
    result["timestamp"] = response_item[0]
    result["player"] = player
    subject, category = table.split(".")
    items = ({TABLE_MAP[category]: item} for item in response_item[1:])
    result[subject] = dict(zip(skills, items))
    return result


def _mergedicts(dict1, dict2):
    """Merge two dictionaries."""
    # Source: https://stackoverflow.com/a/7205672/5231520
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(_mergedicts(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])

def merge_dicts(d1, d2):
    return dict(_mergedicts(d1, d2))


def get_dynamo_rows(player, boundaries):
    """Query RDS for a player/time range and create rows to insert into DDB."""
    logging.info(f"Processing {player}, {boundaries}")
    responses = list()
    for table_name in (f"skills.{col}" for col in HISCORES_RESPONSE_SKILL_COLS):
        logging.info(f"Querying {table_name}")
        sql = build_sql(table_name, HISCORES_RESPONSE_SKILLS, player, boundaries)
        resp = requests.get(API, params=dict(sql=sql))
        items = resp.json()
        parsed_items = [parse_response_item(item, table_name, HISCORES_RESPONSE_SKILLS, player) for item in items]
        responses.append(parsed_items)
    merged_responses = [reduce(merge_dicts, response) for response in zip(*responses)]
    return merged_responses


def get_time_boundaries(start: str, end: str):
    """Convert start,end to monthly tuples."""
    # Source: https://stackoverflow.com/a/34898764/5231520
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    months = list(
        OrderedDict(
            (
                (start_dt + timedelta(_)).strftime("%Y-%m"),
                None
            ) for _ in range((end_dt-start_dt).days)
        ).keys()
    )
    return [[months[i], months[i+1]] for i in range(len(months)-1)]


def main():
    """Read from RDS, parse, and insert into DDB.

    Strategy: work 1 month at a time, and sleep 1 minute in between batch
    inserts to avoid DDB throttling.

    """
    for player in PLAYERS:
        logging.info(f"Beginning {player}")
        for i, boundaries in enumerate(get_time_boundaries(*TABLE_START_END)):
            result = get_dynamo_rows(player, boundaries)
            n = len(result)
            if n > 0:
                logging.info(f"Got result length {n}. Example: {result[0]}")
            else:
                logging.warning(f"Received no results from DB.")

            ## INSERT INTO TABLE

            if i > 0:
                break


if __name__ == "__main__":
    main()
