import json
import logging

import rs_api

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def handler(event, context):
    """Call HiScores API and parse response."""

    player = event["player"]
    logger.info(f"Getting hiscores for {player}")
    payload = rs_api.process_hiscores_response(
        rs_api.request_hiscores(player=player, timeout=45.0)
    )
    return json.dumps(payload)
