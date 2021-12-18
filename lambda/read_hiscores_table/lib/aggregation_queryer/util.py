import decimal
import enum
import json
from datetime import datetime

DAILY_SENTINEL = "Daily#"
TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"
DATE_FMT = "%Y-%m-%d"


class AggregationLevel(enum.Enum):
    NONE = 0
    DAILY = 1


class CustomEncoder(json.JSONEncoder):
    """JSON encode Decimal objects."""

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        if isinstance(o, AggregationLevel):
            return str(o)
        return super(CustomEncoder, self).default(o)


def valid_datetime(date_string, format):
    """Check if a string is a valid datetime."""
    try:
        return datetime.strptime(date_string, format)
    except ValueError:
        return None


def timestamp_to_date(timestamp):
    """Parse a date from a timestamp."""
    # return datetime.strptime(timestamp, TIMESTAMP_FMT).strftime(DATE_FMT)
    return timestamp.split()[0]


def infer_aggregation_level(start_time, end_time):
    """Infer an aggregation level from startTime and endTime parameters"""
    # If times aren't specified, use DAILY aggregation
    if valid_datetime(start_time, DATE_FMT) and valid_datetime(end_time, DATE_FMT):
        return AggregationLevel.DAILY

    # If times are > 1 week apart, use DAILY aggregation
    if (
        valid_datetime(end_time, TIMESTAMP_FMT)
        - valid_datetime(start_time, TIMESTAMP_FMT)
    ).days >= 7:
        return AggregationLevel.DAILY

    # else, use NONE aggregation
    return AggregationLevel.NONE


def get_query_boundaries(start_time, end_time, aggregation_level=AggregationLevel.NONE):
    """Get start and end sort keys for table query."""

    if aggregation_level == AggregationLevel.NONE:
        return start_time, end_time
    elif aggregation_level == AggregationLevel.DAILY:
        return (
            f"{DAILY_SENTINEL}{timestamp_to_date(start_time)}",
            f"{DAILY_SENTINEL}{timestamp_to_date(end_time)}",
        )
    else:
        raise ValueError(f"Unsupported aggregation_level '{aggregation_level}.")


def normalize_nested_dict(d, denom):
    """Normalize values in a nested dict by a given denominator.

    Examples:
    >>> d = {"one": 1.0, "two": {"three": 3.0, "four": 4.0}}
    >>> normalize_nested_dict(d, 2.0)
    {'one': 0.5, 'two': {'three': 1.5, 'four': 2.0}}

    """
    result = dict()
    for key, value in d.items():
        if isinstance(value, dict):
            result[key] = normalize_nested_dict(value, denom)
        else:
            result[key] = value / denom
    return result


def lint_items(items, aggregation_level):
    """Lint items returned from HiScores Table Query."""
    result = list()
    for item in items:
        if aggregation_level == AggregationLevel.NONE:
            # If no aggregation, no action needed
            pass
        elif aggregation_level == AggregationLevel.DAILY:
            item["timestamp"] = item["timestamp"][len(DAILY_SENTINEL) :]
            divisor = item.pop("divisor")
            item["skills"] = normalize_nested_dict(item["skills"], divisor)
            item["activities"] = normalize_nested_dict(item["activities"], divisor)
        else:
            raise ValueError(f"Unsupported aggregation_level '{aggregation_level}.")

        item["aggregationLevel"] = aggregation_level
        result.append(item)

    return result
