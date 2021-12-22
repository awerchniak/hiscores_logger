import json
import logging
import os

import boto3

sqs = boto3.client("sqs")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def handler(event, context):
    with open("orchestrator/players.txt") as players_file:
        player_list = [
            line.strip().replace(" ", "-") for line in players_file.readlines()
        ]

    # send {"player": player} n times to SQS
    logger.info(f"Sending messages for players: {player_list}")
    sqs.send_message_batch(
        QueueUrl=os.environ["GET_AND_PARSE_QUEUE_URL"],
        Entries=[
            dict(
                Id=f"get_and_parse_for_{player}",
                MessageBody=json.dumps({"player": player}),
            )
            for player in player_list
        ],
    )

    return {
        "statusCode": 200,
        "body": json.dumps([player.replace("-", " ") for player in player_list]),
    }
