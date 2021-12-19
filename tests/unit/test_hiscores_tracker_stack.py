import aws_cdk as core
import aws_cdk.assertions as assertions

from hiscores_tracker.hiscores_tracker_stack import HiscoresTrackerStack


def test_sqs_queue_created():
    app = core.App()
    stack = HiscoresTrackerStack(app, "hiscores-logger")
    template = assertions.Template.from_stack(stack)  # noqa: F841


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
