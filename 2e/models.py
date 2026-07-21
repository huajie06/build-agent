from dataclasses import dataclass
from typing import Literal, Any


@dataclass
class SystemMessage:
    role: Literal["system"]
    content: str

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
        }


@dataclass
class UserMessage:
    role: Literal["user"]
    content: str

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
        }


@dataclass
class ToolCall:
    id: str
    name: str
    args: dict[str, Any]

    def to_dict(self):
        return {"id": self.id, "name": self.name, "args": self.args}


@dataclass
class AssistantMessage:
    role: Literal["assistant"]
    content: str | None = None
    reasoning: str | None = None
    tool_calls: list[ToolCall] | None = None
    finish_reason: str | None = None

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "reasoning": self.reasoning,
            "tool_calls": [tool_call.to_dict() for tool_call in self.tool_calls]
            if self.tool_calls is not None
            else None,
            "finish_reason": self.finish_reason,
        }


@dataclass
class ToolMessage:
    role: Literal["tool"]
    tool_call_id: str
    content: str
    name: str | None = None

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "tool_call_id": self.tool_call_id,
            "content": self.content,
            "name": self.name,
        }


Message = SystemMessage | UserMessage | AssistantMessage | ToolMessage


## updated on 2e: isolote tool registry


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]
