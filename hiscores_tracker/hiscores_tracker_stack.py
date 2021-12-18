from aws_cdk import (
    Stack,
)
from constructs import Construct

from .agg_time_series_table import AggregatingTimeSeriesTable
from .hiscores_logger import HiScoresLogger


class HiscoresTrackerStack(Stack):
    """Track your OldSchoolRuneScape HiScores metrics over time."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        # Provision HiScores AggregatingTimeSeriesTable
        atst = AggregatingTimeSeriesTable(self, "HiScoresATST")

        # Provision HiScores API Logger
        HiScoresLogger(self, "OSRSHiScoresLogger", table=atst.table)
