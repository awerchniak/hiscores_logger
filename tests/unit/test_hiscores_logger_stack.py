import aws_cdk as core
import aws_cdk.assertions as assertions

from hiscores_tracker.hiscores_tracker_stack import HiscoresTrackerStack

# example tests. To run these tests, uncomment this file along with the example
# resource in hiscores_logger/hiscores_logger_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HiscoresTrackerStack(app, "hiscores-logger")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
