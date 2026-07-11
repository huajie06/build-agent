import httpx
from config import DEEPSEEK_API_KEY, DEEPSEEK_URL, MODEL
from tools import DEEPSEEK_TOOLS
from models import Message, AssistantMessage

from provider_deepseek import to_deepseek_messages, from_deepseek_assistant_message


def call_llm(messages: list[Message]) -> AssistantMessage:
    api_messages = to_deepseek_messages(messages)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }

    payload = {
        "messages": api_messages,
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

    data = response.json()
    choice = data["choices"][0]

    return from_deepseek_assistant_message(choice)
