from aws_cdk import (
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_sources,
    aws_sqs as sqs,
    Duration,
    Stack,
)
from constructs import Construct
from tempfile import TemporaryDirectory
import os
import subprocess

from .atst import AggregatingTimeSeriesTable


class HiscoresTrackerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Construct a HiscoresTrackerStack."""

        super().__init__(scope, construct_id, **kwargs)

        # Provision HiScores AggregatingTimeSeriesTable
        atst = AggregatingTimeSeriesTable(self, "HiScoresATST")

        # Provision GetAndParseHiScores Lambda
        code_dir = "lambda/get_and_parse_hiscores"
        function_name = "GetAndParseHiScoresLambda"
        with TemporaryDirectory() as layer_output_dir:
            get_and_parse_handler = _lambda.Function(
                self,
                function_name,
                description="Retrieve, parse, and save HiScores data for a given player.",
                runtime=_lambda.Runtime.PYTHON_3_8,
                code=_lambda.Code.from_asset(code_dir),
                handler="get_and_parse_hiscores.handler",
                environment={
                    "HISCORES_TABLE_NAME": atst.table.table_name,
                },
                layers=[
                    self.create_dependencies_layer(
                        layer_id=f"{self.stack_name}-{function_name}-dependencies",
                        requirements_file=os.path.join(code_dir, "requirements.txt"),
                        output_dir=layer_output_dir,
                    )
                ],
            )
        atst.table.grant_write_data(get_and_parse_handler)

        # Provision GetAndParseForPlayer Queue
        get_and_parse_queue = sqs.Queue(
            self, "GetAndParseForPlayerQueue", retention_period=Duration.days(1)
        )
        get_and_parse_handler.add_event_source(
            lambda_event_sources.SqsEventSource(get_and_parse_queue, batch_size=1)
        )

        # Create Orchestrator Lambda
        orchestrator_handler = _lambda.Function(
            self,
            "OrchestratorLambda",
            description="Read configuration and kick off HiScores tracking.",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("lambda/orchestrator"),
            handler="orchestrator.handler",
            environment={"GET_AND_PARSE_QUEUE_URL": get_and_parse_queue.queue_url},
        )
        get_and_parse_queue.grant_send_messages(orchestrator_handler)

        # Create Event to trigger Orchestrator on schedule
        rule = events.Rule(
            self,
            "OrchestratorTrigger",
            description="Trigger Orchestrator Lambda.",
            enabled=True,
            schedule=events.Schedule.cron(
                minute="*/30",  # Trigger every 30 minutes
                hour="0-2,7-23",  # Trigger between 7am and 2am
            ),
        )
        rule.add_target(targets.LambdaFunction(orchestrator_handler))

    def create_dependencies_layer(
        self, layer_id: str, requirements_file: str, output_dir: str
    ) -> _lambda.LayerVersion:
        """Create LambdaLayer with required dependencies.

        Citation: https://github.com/esteban-uo/aws-cdk-python-application-dependencies
        """

        subprocess.check_call(
            f"pip install -r {requirements_file} -t {output_dir}/python".split()
        )
        layer_code = _lambda.Code.from_asset(output_dir)
        return _lambda.LayerVersion(self, layer_id, code=layer_code)
