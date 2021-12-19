import os
import shutil
from contextlib import contextmanager
from tempfile import TemporaryDirectory

from aws_cdk import aws_lambda as _lambda
from aws_cdk.aws_lambda_python import PythonFunction


@contextmanager
def wraps_code_dir(code_dir):
    """Copy a code directory into a temporary directory."""
    with TemporaryDirectory() as tmp_dir:
        new_path = os.path.join(tmp_dir, os.path.basename(code_dir))
        shutil.copytree(code_dir, new_path)
        yield tmp_dir


def package_lambda(
    scope,
    handler_name,
    function_name,
    description,
    environment=None,
    retry_attempts=None,
):
    """Package handler source and provision Lambda function."""
    original_code_dir = os.path.join("lambda", handler_name)
    with wraps_code_dir(code_dir=original_code_dir) as code_dir:
        return PythonFunction(
            scope,
            function_name,
            entry=os.path.join(code_dir, "handler.py"),
            descrtion=description,
            runtime=_lambda.Runtime.PYTHON_3_8,
            environment=environment,
            retry_attempts=retry_attempts,
        )
