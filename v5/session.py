from Pathlib import Path
from models import Message, SystemMessage, UserMessage, AssistantMessage, ToolMessage
import json


def parse_message(data: dict) -> Message:
    role = data.get("role")

    if role == "system":
        return SystemMessage(**data)
    elif role == "user":
        return UserMessage(**data)
    elif role == "assistant":
        return AssistantMessage(**data)
    elif role == "tool":
        return ToolMessage(**data)
    else:
        raise ValueError(f"Unknown message role: {role}")


def save_session(data: list[Message], path: str):
    p = Path(path)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)

        with p.open("w", encoding="utf-8") as f:
            json.dump([d.to_dict() for d in data], f, indent=4)

    except Exception as e:
        print(f"An error has occured: {e}, session save filed")


def load_session(path: str):
    p = Path(path)

    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return [parse_message(d) for d in data]

    except Exception as e:
        print(f"An error has occured: {e}, session load filed")
