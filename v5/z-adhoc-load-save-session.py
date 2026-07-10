from models import Message, SystemMessage, UserMessage, AssistantMessage, ToolMessage
import json
from session import save_session, load_session

raw_messages = r"""
[
    {
        "role": "system",
        "content": "You are a helpful assistant"
    },
    {
        "role": "user",
        "content": "write joke to my current folder, called joke_01.txt"
    },
    {
        "role": "assistant",
        "content": "Here's a fun joke for you!",
        "reasoning": "The user wants me to write a joke to a file called \"joke_01.txt\" in the current folder. Let me create a funny joke and write it to that file.",
        "tool_calls": [
            {
                "index": 0,
                "id": "call_00_wTWHg9V1FefFiNdmbX3h7102",
                "type": "function",
                "function": {
                    "name": "write_text_file",
                    "arguments": "{\"path\": \"joke_01.txt\", \"content\": \"Why don't scientists trust atoms?\\n\\nBecause they make up everything! \ud83d\ude04\\n\"}"
                }
            }
        ]
    },
    {
        "role": "tool",
        "tool_call_id": "call_00_wTWHg9V1FefFiNdmbX3h7102",
        "content": "{\"result\": \"Wrote 70 characters to joke_01.txt\"}"
    },
    {
        "role": "assistant",
        "content": "Done! I've written a joke to **joke_01.txt** in your current folder. Here's what's inside:\n\n> Why don't scientists trust atoms?\n> \n> Because they make up everything! \ud83d\ude04\n\nFeel free to open it anytime for a quick laugh!"
    }
]
"""

m: list[Message] = []


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


# data = json.loads(raw_messages)
# for d in data:
#     parsed_result = parse_message(d)
#     m.append(parsed_result)

# save_session(m, "./session/data.json")

session_data = load_session("./session/data.json")
for s in session_data:
    print(s)
    print("-" * 20)

# with open("./session/data.json") as f:
#     data = json.load(f)

# for d in data:
#     if d.get("role") == "assistant":
#         print(d)
