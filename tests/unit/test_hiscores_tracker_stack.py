import aws_cdk as core
import aws_cdk.assertions as assertions

from hiscores_tracker.hiscores_tracker_stack import HiscoresTrackerStack


def test_synthesize():
    app = core.App()
    stack = HiscoresTrackerStack(app, "hiscores-logger")
    template = assertions.Template.from_stack(stack)

    # Assert no extraneous resources
    template.resource_count_is("AWS::Lambda::Function", 4)
    template.resource_count_is("AWS::DynamoDB::Table", 1)
    template.resource_count_is("AWS::SQS::Queue", 1)
    template.resource_count_is("AWS::ApiGateway::RestApi", 2)
    template.resource_count_is("AWS::Events::Rule", 1)

    # Test HiScoresTable created
    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "KeySchema": [
                {"AttributeName": "player", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            "AttributeDefinitions": [
                {"AttributeName": "player", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            "SSESpecification": {"SSEEnabled": True},
            "StreamSpecification": {"StreamViewType": "NEW_IMAGE"},
        },
    )

    # Test Orchestrator created
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "orchestrator.handler.handler",
            "Runtime": "python3.8",
        },
    )

    # Test GetAndParse created
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "get_and_parse_hiscores.handler.handler",
            "Runtime": "python3.8",
        },
    )

    # Test Aggregator created
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "aggregator.handler.handler",
            "Runtime": "python3.8",
        },
    )

    # Test Queryer created
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "read_hiscores_table.handler.handler",
            "Runtime": "python3.8",
        },
    )
