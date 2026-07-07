from dataclasses import dataclass
from typing import Literal


@dataclass
class Message:
    role: Literal["system", "assistant", "user"]
    content: str

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, dict):
        if dict.get("role") == "tool":
            return dict

        role = dict.get("role", "")
        content = dict.get("content", "")
        return cls(role=role, content=content)
