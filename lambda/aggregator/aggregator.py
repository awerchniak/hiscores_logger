import boto3
import logging
import os

from util import (
    aggregate_hiscores_rows,
    lint_query_response,
    parse_image,
    unroll_image,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["HISCORES_TABLE_NAME"])

DAILY_SENTINEL = "Daily#"


def _timestamp_to_date(timestamp):
    """Parse a date from a timestamp."""
    # TIMESTAMP = "%Y-%m-%d %H:%M:%S"
    # DATE = "%Y-%m-%d"
    # return datetime.strptime(timestamp, TIMESTAMP).strftime(DATE)
    return timestamp.split()[0]


def handler(event, context):
    event_name = event["Records"][0]["eventName"]
    event_source = event["Records"][0]["eventSource"]
    logger.info(f"Processing Event '{event_name}' from source '{event_source}'.")

    if event_name == "INSERT":
        new_image = event["Records"][0]["dynamodb"]["NewImage"]
        player_id, timestamp = parse_image(new_image)
        if timestamp.startswith(DAILY_SENTINEL):
            logger.info("Ignoring event from daily aggregation write.")
            return

        logger.info(f"Received image: {new_image}")

        timestamp = f"{DAILY_SENTINEL}{_timestamp_to_date(timestamp)}"
        logger.info(f"Processing daily aggregation for {player_id}:{timestamp}.")

        unrolled_new_image = unroll_image(new_image)
        unrolled_new_image["timestamp"] = timestamp
        unrolled_new_image["divisor"] = 1
        logger.info(f"Formatted incoming row: {unrolled_new_image}")

        key = {"player": player_id, "timestamp": timestamp}
        logger.info(f"Querying table for {key}")
        resp = table.get_item(Key=key)
        logger.info(f"Received response {resp}")

        linted_resp = lint_query_response(resp["Item"]) if "Item" in resp else None
        logger.info(f"Linted response: {linted_resp}")

        new_item = aggregate_hiscores_rows(linted_resp, unrolled_new_image)
        logger.info(f"Produced aggregation {new_item}")

        table.put_item(Item=new_item)

        return new_item
    else:
        logger.info("Ignoring non-insert event.")
