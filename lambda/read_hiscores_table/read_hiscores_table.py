import boto3
import os
from boto3.dynamodb.conditions import Key

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["HISCORES_TABLE_NAME"])


def handler(event, context):
    """Query table and return result."""
    if "player" not in event:
        raise ValueError("Invocation must include 'player' attribute.")
    player = event["player"]

    if "timeRange" not in event or len(event["timeRange"]) != 2:
        raise ValueError(
            "Invocation must include 'timeRange' attribute "
            'with shape ["YYYY-mm-dd HH:MM:SS","YYYY-mm-dd HH:MM:SS"].'
        )
    time_range = event["timeRange"]

    response = table.query(
        KeyConditionExpression=Key("player").eq(player)
        & Key("timestamp").between(*time_range)
    )
    return response["Items"]
