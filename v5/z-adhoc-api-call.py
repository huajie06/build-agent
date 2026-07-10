from models import SystemMessage, UserMessage, Message
from config import DEEPSEEK_URL, DEEPSEEK_API_KEY, MODEL
from tools import DEEPSEEK_TOOLS
import httpx

messages = [SystemMessage(role="system", content="You are a helpful assistant")]
messages.append(
    UserMessage(role="user", content="read my file agent.py at current path")
)

print([msg.to_dict() for msg in messages])


def call_DeepSeek(messages: list[dict] | list[Message]) -> dict:
    """Call DeepSeek API, with default configs

    This design lets exceptions propagate, instead of using try/except block here.
    """

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }

    payload = {
        "messages": [msg.to_dict() for msg in messages],
        "model": MODEL,
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "max_tokens": 4096,
        "response_format": {"type": "text"},
        "stream": False,
        "temperature": 1,
        "top_p": 1,
        "tools": DEEPSEEK_TOOLS,
        "tool_choice": "auto",
        "logprobs": False,
    }

    response = httpx.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()


result = call_DeepSeek(messages)

print(result)
