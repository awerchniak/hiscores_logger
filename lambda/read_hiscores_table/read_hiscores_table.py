import boto3
import os
from boto3.dynamodb.conditions import Key

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["HISCORES_TABLE_NAME"])


def handler(event, context):
    """Query table and return result."""
    player = event["player"]
    time_range = event["timeRange"]

    response = table.query(
        KeyConditionExpression=Key("player").eq(player)
        & Key("timestamp").between(*time_range)
    )
    return response["Items"]
