import pytest

import aggregator.lib.dynamo_aggregator.util as util


def test_aggregate_dictlikes():
    a = {
        "hi": {
            "hello": {
                "sup": 10,
                "how": 4,
            },
            "sup": {
                "nothin": 5,
                "nmu": 12,
            },
        },
        "yo": {
            "sup": 7,
        },
    }
    b = {
        "hi": {
            "hello": {
                "sup": 3,
                "how": 13,
            },
            "sup": {
                "nothin": 6,
                "nmu": 1,
            },
        },
        "yo": {
            "sup": 20,
            "whats poppin": 5,
        },
    }
    expected = {
        "hi": {
            "hello": {
                "sup": 13,
                "how": 17,
            },
            "sup": {
                "nothin": 11,
                "nmu": 13,
            },
        },
        "yo": {
            "sup": 27,
        },
    }
    result = util.aggregate_dictlikes(a, b)
    assert result == expected


def test_aggregate_dictlikes_incomplete_b():
    with pytest.raises(util.SchemaMismatch):
        util.aggregate_dictlikes({"a": 2}, {})


def test_aggregate_dictlikes_invalid_b():
    with pytest.raises(util.SchemaMismatch):
        util.aggregate_dictlikes({"a": 2}, {"a": "two"})


def test_aggregate_hiscores_rows_none():
    new_data = {}
    assert util.aggregate_hiscores_rows(None, new_data) == new_data


def test_aggregate_hiscores_rows():
    linted_response = {
        "divisor": 4,
        "activities": {
            "TheatreofBlood": {
                "kc": -4,
                "rnk": -4,
            },
        },
        "skills": {
            "Overall": {
                "xp": 4000000,
                "rnk": 4000000,
                "lvl": 4000,
            }
        },
        "player": "PlayerName",
        "timestamp": "Daily#2021-12-17",
    }
    unrolled_new_image = {
        "divisor": 1,
        "activities": {
            "TheatreofBlood": {
                "kc": -1,
                "rnk": -1,
            },
        },
        "skills": {
            "Overall": {
                "xp": 1000000,
                "rnk": 1000000,
                "lvl": 1000,
            }
        },
        "player": "PlayerName",
        "timestamp": "2021-12-17 22:00:00",
    }
    result = util.aggregate_hiscores_rows(linted_response, unrolled_new_image)
    assert result == {
        "divisor": 5,
        "activities": {
            "TheatreofBlood": {
                "kc": -5,
                "rnk": -5,
            },
        },
        "skills": {
            "Overall": {
                "xp": 5000000,
                "rnk": 5000000,
                "lvl": 5000,
            }
        },
        "player": "PlayerName",
        "timestamp": "Daily#2021-12-17",
    }
