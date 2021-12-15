"""Utility functions for aggregator lambda."""
from decimal import Decimal


class SchemaMismatch(ValueError):
    """Schemas of nested dicts do not match."""


def aggregate_dictlikes(a, b, aggregation_fn=lambda a, b: a + b, _key_path=""):
    """Aggregate nested dict-likes, preserving schema.

    Adds to a nested aggregation with values from a second dict-like containing
    the same keys. While the second object must contain all of the keys in the
    aggregation, it may contain additional keys. These will be ignored.

    Args:
        a (dict): First dict-like to aggregate.
        b (dict): Second dict-like to aggregate.
        aggregation_fn (Callable): Two-item aggregation operation.

    Returns:
        dict

    """
    result = dict()
    for key, a_val in a.items():
        new_key_path = _key_path + "_" + key
        if key not in b:
            raise SchemaMismatch(
                f"Expected key '{new_key_path}' does not exist in object b."
            )
        b_val = b[key]
        a_val_type = type(a_val)
        b_val_type = type(b_val)
        if a_val_type != b_val_type:
            raise SchemaMismatch(
                f"Key '{new_key_path}' of type '{b_val_type}' does not match "
                f"expected type of '{a_val_type}'"
            )
        if isinstance(a_val, dict):
            result[key] = aggregate_dictlikes(
                a_val,
                b_val,
                aggregation_fn=aggregation_fn,
                _key_path=new_key_path,
            )
        else:
            result[key] = aggregation_fn(a_val, b_val)
    return result


def aggregate_hiscores_rows(sum_row, new_data):
    """Add new_data to a sum row."""
    if sum_row is None:
        return new_data
    player_id = sum_row.pop("player")
    timestamp = sum_row.pop("timestamp")
    aggregation = aggregate_dictlikes(sum_row, new_data)
    aggregation["player"] = player_id
    aggregation["timestamp"] = timestamp
    return aggregation


"""
Utility functions for unrolling DDB images.
"""


def _image_map(_map):
    return dict(_map["M"])


def _image_num(_map):
    return int(_map["N"])


def _image_str(_map):
    return str(_map["S"])


"""
\\Utility functions.
"""


def parse_image(image):
    """Parse player ID and timestamp from a DDB event image."""
    return _image_str(image["player"]), _image_str(image["timestamp"])


def unroll_image(image):
    """Convert DDBEvent to Item schema."""
    unrolled = dict()
    for k, v in image.items():
        if isinstance(v, dict):
            if "M" in v:
                unrolled[k] = unroll_image(_image_map(v))
            elif "S" in v:
                unrolled[k] = _image_str(v)
            elif "N" in v:
                unrolled[k] = _image_num(v)
        else:
            unrolled[k] = v
    return unrolled


def cast_nested_dict(d, original_type, new_type):
    """Cast items in a nested dict to a new type.

    Converts all leaves of type `original_type` to type `new_type`

    Args:
        d (dict): nested dict to cast
        original_type (type): old type to convert
        new_type (type): new type to apply to leaf nodes

    Returns:
        dict

    """
    result = dict()
    for k, v in d.items():
        if isinstance(v, dict):
            result[k] = cast_nested_dict(
                v, original_type=original_type, new_type=new_type
            )
        elif isinstance(v, original_type):
            result[k] = new_type(v)
        else:
            result[k] = v
    return result


def lint_query_response(item):
    """Convert query response to nested dict of ints."""
    return cast_nested_dict(d=item, original_type=Decimal, new_type=int)
