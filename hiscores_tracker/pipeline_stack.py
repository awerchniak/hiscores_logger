from constructs import Construct
from aws_cdk import Stack, pipelines


class HiScoresTrackerPipelineStack(Stack):
    """CI/CD Pipeline for HiScoresTracker project."""

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection("awerchniak/cdk-hiscores-tracker", "cicd",
                    connection_arn="arn:aws:codestar-connections:us-east-1:212039253172:connection/72414c8f-a6e4-427c-a701-a38759440114"
                ),
                commands=[
                    "npm install -g aws-cdk@2.0.0",
                    "pip install -r requirements.txt",
                    "cdk synth",
                ]
            ),
        )
