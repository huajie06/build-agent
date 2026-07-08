from dataclasses import dataclass
from typing import Literal


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
class AssistantMessage:
    role: Literal["assistant"]
    content: str | None = None
    reasoning_content: str | None = None
    tool_calls: list[dict] | None = None
    finish_reason: str | None = None

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "reasoning": self.reasoning_content,
            "tool_calls": self.tool_calls,
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
