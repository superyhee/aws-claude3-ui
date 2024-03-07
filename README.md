# AWS Bedrock Chat UI using Claude 3 model

What does it do?

- Creates an AWS Lambda function that interacts with AWS Bedrock

- Uses Anthropic's Claude 3 Sonnet model for chat

- Creates an AWS API Gateway endpoint to expose the API

- Deploy a chat ui on AWS

Install Guide

1.Automatically deploy api gateway and lambda and call bedrock through lambda.

- `npm i` install required libray

- `cdk deploy` deploy this stack to your default AWS account/region

- `cdk diff` compare deployed stack with current state

- `cdk synth` emits the synthesized CloudFormation template

  2.deploy ui
