from constructs import Construct
from aws_cdk import Stage

from .hiscores_tracker_stack import HiscoresTrackerStack


class HiscoresTrackerPipelineStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = HiscoresTrackerStack(self, "WebService")
