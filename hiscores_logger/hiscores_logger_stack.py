from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
)
from constructs import Construct
from tempfile import TemporaryDirectory
import os
import subprocess


class HiscoresLoggerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Construct a HiscoresLoggerStack."""

        super().__init__(scope, construct_id, **kwargs)

        code_dir = "lambda"
        function_name = "GetAndParseOSRSMetricsLambda"

        with TemporaryDirectory() as layer_output_dir:
            _lambda.Function(
                self,
                function_name,
                runtime=_lambda.Runtime.PYTHON_3_8,
                code=_lambda.Code.from_asset(code_dir),
                handler="get_and_parse_metrics.handler",
                layers=[
                    self.create_dependencies_layer(
                        layer_id=f"{self.stack_name}-{function_name}-dependencies",
                        requirements_file=os.path.join(code_dir, "requirements.txt"),
                        output_dir=layer_output_dir,
                    )
                ],
            )

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
