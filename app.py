#!/usr/bin/env python3
import os

import aws_cdk as cdk

from hiscores_tracker.pipeline_stack import HiScoresTrackerPipelineStack


app = cdk.App()
HiScoresTrackerPipelineStack(app, "HiScoresTrackerPipelineStack")

app.synth()
