from dataclasses import dataclass
from typing import Any, Literal, TypeAlias


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


ConversationItem: TypeAlias = Message | ToolCall | ToolResult

messages: list[ConversationItem] = []

messages.append(
    Message(
        role="user",
        content="What's the time now in NYC?",
    )
)

messages.append(
    ToolCall(
        id="tool_001",
        name="find_nyc_time",
        arguments={"loc": "nyc"},
    )
)

messages.append(
    ToolResult(
        call_id="tool_001",
        content="19:30",
    )
)

messages.append(
    Message(
        role="assistant",
        content="The current time is 19:30.",
    )
)

for m in messages:
    print(m)
