# Copyright iX.
# SPDX-License-Identifier: MIT-0
import os
from utils import bedrock


# os.environ["BEDROCK_ASSUME_ROLE"] = "<YOUR_ROLE_ARN>"  # E.g. "arn:aws:..."
# 推荐使用 IAM role 授权方式
# Create new bedrock client
bedrock_runtime = bedrock.get_bedrock_client(
    assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
    region=os.environ.get("AWS_DEFAULT_REGION", "us-west-2"),
)

boto3_bedrock = bedrock.get_bedrock_client(
    assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
    region=os.environ.get("AWS_DEFAULT_REGION", "us-west-2"),
    runtime=False
)


def test_connection():
    # Validate the connection
    model_list = boto3_bedrock.list_foundation_models()
    return model_list


def text_image(name, message, history):
    history = history or []
    message = message.lower()
    salutation = "Good morning" if message else "Good evening"
    greeting = f"{salutation} {name}. {message} degrees today"
    return greeting
