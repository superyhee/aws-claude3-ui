# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
"""General helper utilities here"""
# Python Built-Ins:
from io import StringIO
import re
import sys
import json
import textwrap


def print_ww(*args, width: int = 100, **kwargs):
    """Like print(), but wraps output to `width` characters (default 100)"""
    buffer = StringIO()
    try:
        _stdout = sys.stdout
        sys.stdout = buffer
        print(*args, **kwargs)
        output = buffer.getvalue()
    finally:
        sys.stdout = _stdout
    for line in output.splitlines():
        print("\n".join(textwrap.wrap(line, width=width)))


def format_resp(response:str):
    """Format the output content, remove xml tags"""
    # Trims leading whitespace using regular expressions
    pattern = '^\\s+'
    response = re.sub(pattern, '', response)
    # Remove XML tags using regular expressions
    # response = response[response.index('\n')+1:]
    match = response.startswith('<')
    if match:
        return re.sub(r'<[^>]+>', '', response)
    else:
        return response


MESSAGE_TYPES = ("text", "image")

def format_message(content, role, msg_type):

    if msg_type not in MESSAGE_TYPES:
        raise ValueError(f"Invalid message type: {msg_type}")

    base_msg = {"role": role, "content": []}

    match msg_type:
        case "text":
            base_msg["content"] = [{"type": "text", "text": content}]
        case "image":
            base_msg["content"] = [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": content
                    }
                },
                {
                    "type": "text",
                    "text": "Describe what you understand from the content in this picture, as much detail as possible."
                }
            ]
        case _:                      
            pass

    return base_msg


# Helper function to pass prompts and inference parameters
def generate_content(runtime, messages, system, params, model_id):
    params['system'] = system
    params['messages'] = messages
    body=json.dumps(params)
    
    response = runtime.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())

    return response_body


class ChatHistory:
    """Abstract class for storing chat message history."""

    def __init__(self, initial_history=None):
        """
        Initialize a ChatHistoryMemory instance.        
        Args:
            initial_messages (list, optional): List of initial chat messages. Defaults to None.
        """
        self.messages = []
        if initial_history:
            for user_msg, assistant_msg in initial_history:
                self.add_user_text(user_msg)
                self.add_bot_text(assistant_msg)

    def add_message(self, message) -> None:
        """Add a message to the history list"""
        self.messages.append(message)

    def clear(self) -> None:
        """Clear memory"""
        self.messages.clear()

    def add_user_text(self, message: str) -> None:
        self.add_message(
            format_message(message, "user", 'text')                    
        )

    def add_user_image(self, message: str) -> None:
        self.add_message(
            format_message(message, "user", 'image')                    
        )

    def add_bot_text(self, message: str) -> None:
        self.add_message(
            format_message(message, "assistant", 'text')                    
        )

    def add_bot_image(self, message: str) -> None:
        self.add_message(
            format_message(message, "assistant", 'image')                    
        )

    def get_latest_message(self):
        return self.messages[-1] if self.messages else None
