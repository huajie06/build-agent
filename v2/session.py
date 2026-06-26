import json
from pathlib import Path


def save_session(messages: list[dict], path: Path):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(messages, file, indent=4)
    except Exception as e:
        print(f"An error has occurred: {e}, session save failed")


def load_session(path: Path) -> list[dict] | None:
    try:
        with path.open("r", encoding="utf-8") as file:
            messages = json.load(file)
        return messages
    except Exception as e:
        print(f"An error has occurred: {e}, session load failed")
        return None
