import json
from pathlib import Path
from models import Message
from llm import serialize_message


def save_session(messages: list[dict] | list[Message], path: Path):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump([serialize_message(msg) for msg in messages], file, indent=4)
    except Exception as e:
        print(f"An error has occurred: {e}, session save failed")


def load_session(path: Path) -> list[dict] | None:
    try:
        with path.open("r", encoding="utf-8") as file:
            raw_messages = json.load(file)
        return [Message.from_dict(msg) for msg in raw_messages]

    except Exception as e:
        print(f"An error has occurred: {e}, session load failed")
        return None
