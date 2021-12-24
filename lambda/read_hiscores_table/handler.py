import json
import logging
import os

import boto3
from boto3.dynamodb.conditions import Key
from read_hiscores_table.lib.aggregation_queryer.util import (
    DATE_FMT,
    MONTH_FMT,
    TIMESTAMP_FMT,
    CustomEncoder,
    get_query_boundaries,
    infer_aggregation_level,
    lint_items,
    valid_datetime,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["HISCORES_TABLE_NAME"])


def handler(event, context):
    """Query table and return result."""

    method = event["httpMethod"]
    if method != "GET":
        return {
            "statusCode": 501,
            "body": json.dumps({"status": 501, "message": "We only accept GET /"}),
        }

    params = event["queryStringParameters"]
    if not isinstance(params, dict):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "status": 400,
                    "message": (
                        "API requires 'player', 'startTime', and 'endTime' params."
                    ),
                }
            ),
        }

    if "player" not in params:
        return {"statusCode": 400, "body": "API requires 'player' param."}
    player = params["player"]

    if "startTime" not in params or not any(
        [
            valid_datetime(params["startTime"], TIMESTAMP_FMT),
            valid_datetime(params["startTime"], DATE_FMT),
            valid_datetime(params["startTime"], MONTH_FMT),
        ]
    ):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "status": 400,
                    "body": (
                        "API requires 'startTime' param with shape "
                        "'YYYY-mm[-dd [HH:MM:SS]]'"
                    ),
                }
            ),
        }
    start_time = params["startTime"]

    if "endTime" not in params or not any(
        [
            valid_datetime(params["endTime"], TIMESTAMP_FMT),
            valid_datetime(params["endTime"], DATE_FMT),
            valid_datetime(params["endTime"], MONTH_FMT),
        ]
    ):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "status": 400,
                    "body": (
                        "API requires 'endTime' param with shape "
                        "'YYYY-mm[-dd [HH:MM:SS]]'"
                    ),
                }
            ),
        }
    end_time = params["endTime"]

    try:
        aggregation_level = infer_aggregation_level(start_time, end_time)
        query_boundaries = get_query_boundaries(start_time, end_time, aggregation_level)
    except TypeError:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "status": 400,
                    "body": "'startTime' and 'endTime' parameter formats must match.",
                }
            ),
        }

    logger.info(
        f"Retrieving HiScores data for player '{player}' between "
        f"{query_boundaries[0]} and {query_boundaries[1]}"
    )
    response = table.query(
        KeyConditionExpression=Key("player").eq(player)
        & Key("timestamp").between(*query_boundaries)
    )
    items = response["Items"]
    logger.info(f"Received items: {items}")

    linted_items = lint_items(items, aggregation_level)
    logger.info(f"Linted items: {linted_items}")

    return {
        "statusCode": 200,
        "body": json.dumps(linted_items, cls=CustomEncoder),
    }
