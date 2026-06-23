"""data send to model API: 3 layers system prompt, tools, message

- system prompt defines the agent
- tools tell what tools are available for assitant to use
- message is the chat history, it includes roles and content block
    + role can be: user, assistant, tool (tool_call vs. tool_result)
    + content block: user message would be str, assistant would be str + tool_call
      then tool_result is the tool results

Note: some AI agent wraps tool_call and tool_result as part of the assitant, and
 user message, which Pi agent does it differently. I like the desing, and will
 stick to that

"""

from dotenv import load_dotenv
import os
from typing import Literal
from dataclasses import dataclass
from Pathlib import Path

load_dotenv("../../.env")
api_key = os.environ.get("DEEPSEEK_API_KEY")
print(api_key)


Role = Literal["system", "user", "assistant", "tool"]


@dataclass
class Message:
    role: Role
    content: str | None = None


msg = []
msg.append(Message("system", "you are a helpful assistant"))
msg.append(Message("user", "tell me a joke"))

for m in msg:
    print(m)


# read and write file tools
def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_file(path: str, content: str) -> str:
    Path(path).write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} characters to {path}"


tool_registry = {
    "read_file": read_file,
    "write_file": write_file,
}


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the text content of a file.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
]
