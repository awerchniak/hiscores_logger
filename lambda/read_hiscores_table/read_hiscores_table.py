import boto3
import json
import logging
import os
from boto3.dynamodb.conditions import Key
from datetime import datetime

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["HISCORES_TABLE_NAME"])

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _valid_datetime(date_string, format="%Y-%m-%d %H:%M:%S"):
    """Check if a string is a valid datetime."""
    try:
        return datetime.strptime(date_string, format)
    except ValueError:
        return None


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
                    "message": "API requires 'player', 'startTime', and 'endTime' params.",
                }
            ),
        }

    if "player" not in params:
        return {"statusCode": 400, "body": "API requires 'player' param."}
    player = params["player"]

    if "startTime" not in params or not _valid_datetime(params["startTime"]):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "status": 400,
                    "body": "API requires 'startTime' param with shape 'YYYY-mm-dd HH:MM:SS'",
                }
            ),
        }
    start_time = params["startTime"]

    if "endTime" not in params or not _valid_datetime(params["endTime"]):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "status": 400,
                    "body": "API requires 'endTime' param with shape 'YYYY-mm-dd HH:MM:SS'",
                }
            ),
        }
    end_time = params["endTime"]

    logger.info(
        f"Retrieving HiScores data for player '{player}' between "
        f"{start_time} and {end_time}"
    )
    response = table.query(
        KeyConditionExpression=Key("player").eq(player)
        & Key("timestamp").between(start_time, end_time)
    )
    logger.info(f"Received data: {response['Items']}")
    return {"statusCode": 200, "body": json.dumps(response["Items"])}
