
# OSRS HiScores Tracking via AWS CDK

This project helps OSRS players to track and visualize their in-game progress using the HiScores API. It is built on Amazon Web Services and is easily bootstrapped using AWS CDK. As such, having an AWS account and the AWS CLI installed is a prerequisite.

To get started, simply clone the repo. Then:
```
aws configure
npm install -g aws-cdk
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
cdk deploy
```

Then, navigate to the AWS Console. You should see your resources created there. To clean up when you're done:
```
cdk destroy
```