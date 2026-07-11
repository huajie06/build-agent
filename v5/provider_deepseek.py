from models import Message, AssistantMessage


def to_deepseek_messages(messages: list[Message]) -> list[dict]:
    """Deepseek API uses `reasoning_content` instead of `content`"""
    api_message = []

    for m in messages:
        m_dict = m.to_dict()
        if m_dict.get("role") == "assistant":
            m_dict["reasoning_content"] = m_dict.pop("reasoning")
        api_message.append(m_dict)

    return api_message


def from_deepseek_assistant_message(choice) -> AssistantMessage:
    """Deepseek API uses `reasoning_content` instead of `content`"""
    deepseek_msg = choice["message"]
    deepseek_msg["reasoning"] = deepseek_msg.pop("reasoning_content")
    deepseek_msg["finish_reason"] = choice.get("finish_reason", None)
    return AssistantMessage(**deepseek_msg)
