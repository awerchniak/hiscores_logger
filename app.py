#!/usr/bin/env python3
import os

import aws_cdk as cdk

from hiscores_logger.hiscores_logger_stack import HiscoresLoggerStack


app = cdk.App()
HiscoresLoggerStack(app, "HiscoresLoggerStack")

app.synth()
