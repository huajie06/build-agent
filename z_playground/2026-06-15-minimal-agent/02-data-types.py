from dataclasses import dataclass
from typing import Literal, Any
from pathlib import Path
import json


@dataclass
class Message:
    role: Literal["system", "user", "assistant"]
    content: str


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    call_id: str
    content: Any
    is_error: bool = False


items: list[Message | ToolCall | ToolResult] = []

items.append(
    Message(
        role="user",
        content="What's the time now in NYC?",
    )
)

items.append(
    ToolCall(
        id="tool_001",
        name="find_nyc_time",
        arguments={"loc": "nyc"},
    )
)

items.append(
    ToolResult(
        call_id="tool_001",
        content="19:30",
    )
)

items.append(
    Message(
        role="assistant",
        content="The current time is 19:30.",
    )
)

for i in items:
    print(i, "\n")


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "read the text content of a file",
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
            "description": "write content to a file.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
]


def to_deepseek():
    pass


def from_deepseek():
    pass


test_text_path = (
    Path("/home/mz/repos/learning/z_playground/2026-06-15-deepseek-api-call-test/")
    / "Response-1781755662363.json"
)

with test_text_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

# print(json.dumps(data, indent=4))


dp_msg = data["choices"][0]["message"]

tool_calls = dp_msg["tool_calls"]
if tool_calls:
    print(tool_calls)


# while True:
#     input_text = input("Enter your question: ")
#     if input_text.trim().lower() == "/exit":
#         break
#     else:
#         pass
