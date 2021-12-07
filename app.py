#!/usr/bin/env python3
import os

import aws_cdk as cdk

from hiscores_tracker.hiscores_tracker_stack import HiscoresTrackerStack


app = cdk.App()
HiscoresTrackerStack(app, "HiscoresTrackerStack")

app.synth()
