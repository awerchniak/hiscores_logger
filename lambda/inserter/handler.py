import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["HISCORES_TABLE_NAME"])


def handler(event, context):
    """Query table and return result."""

    method = event["httpMethod"]
    if method != "POST":
        return {
            "statusCode": 501,
            "body": json.dumps({"status": 501, "message": "We only accept POST /"}),
        }

    params = event["queryStringParameters"]
    if not isinstance(params, dict):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "status": 400,
                    "message": ("API requires 'item' param."),
                }
            ),
        }

    if "item" not in params:
        return {"statusCode": 400, "body": "API requires 'item' param."}
    item = json.loads(params["item"])
    logging.info(f"De-serialized item: {item}")
    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps(item),
    }
