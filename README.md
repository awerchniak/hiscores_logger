
OSRS HiScores Tracking with AWS CDK
====================================
<img src="./assetts/Old_School_RuneScape_logo.png" width=500 />

# Background

This project helps OSRS players to track and visualize their in-game progress using the HiScores API. It is built on Amazon Web Services and is easily bootstrapped using AWS CDK. As such, having an AWS account and the AWS CLI installed is a prerequisite.

# Getting Started

## Prerequisites

1. [Create a free-tier AWS account](https://aws.amazon.com/free) (if you don't already have one)
1. [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. [Configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
3. Install the CDK CLI: `npm install -g aws-cdk@2.0.0`

## Clone the repo

```
git clone https://github.com/awerchniak/cdk-hiscores-tracker.git
cd cdk-hiscores-tracker
```

## Configure
Edit the file located at `lambda/orchestrator/players.txt` to use the usernames of the players you would like to track (minimum: 1).

## Build and deploy

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
cdk deploy
```

At the end of the terminal output, you should see something like:
```
Outputs:
HiscoresTrackerStack.HiScoresATSTQueryHiScoresDataEndpointB5BC150F = https://511h1wh89e.execute-api.us-east-1.amazonaws.com/prod/
```

Your Stack name and URL will be slightly different. Make note of the URL; this is a public API you can call to query your stats database. It takes 3 parameters: `{player: str, startTime: str, endTime: str}`.

You can now navigate to the AWS console and see your resources created. Take a look at the Service Overview below to get oriented. In particular, see DynamoDB and Lambda.

## Cleanup

When you are finished, you can destroy all resources with:

```
cdk destroy
```

# Contributing

We welcome contributions. If you would like to contribute, please fork the repo and issue a pull request with your changes. We will respond to all PRs within a 1 week SLA. Prior to submitting your pull request, ensure all tests are passing.

## Running unit tests
```
pip install -r requirements-dev.txt
bash run_tests.sh
```

# Service overview

<img src="./assetts/service_diagram.png" width=1000 />

The core service is built on two Constructs: `HiScoresLogger` and `AggregatingTimeSeriesTable`. 

The first uses a CloudWatch EventBridge to trigger an Orchestrator Lambda, which reads your configuration file and sends instruction messages to an SQS Queue. A Lambda Function listens to this queue, and when it receives a request for a username, it queries the HiScores API, parses the response, and saves it to a table.

The second is a Dynmo Table with a Lambda Function subscribed to write events. When the table is written to, the Lambda aggregates the new record into a daily sum row. The table also comes with a queryer Lambda Function and API Gateway Endpoint for easy reading with configurable daily aggregation.
