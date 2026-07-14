from models import Message, AssistantMessage


def to_deepseek_message(message: Message) -> dict:
    """FIXED: process internal message for external feed"""
    if message.role in ("system", "user"):
        return {
            "role": message.role,
            "content": message.content,
        }

    if message.role == "assistant":
        result = {
            "role": "assistant",
            "content": message.content,
        }

        if message.reasoning is not None:
            result["reasoning_content"] = message.reasoning

        if message.tool_calls:
            result["tool_calls"] = message.tool_calls

        return result

    if message.role == "tool":
        return {
            "role": "tool",
            "tool_call_id": message.tool_call_id,
            "content": message.content,
        }

    raise ValueError(f"Unsupported message: {message}")


def to_deepseek_messages(messages: list[Message]) -> list[dict]:
    return [to_deepseek_message(m) for m in messages]


# def from_deepseek_assistant_message(choice) -> AssistantMessage:
#     """Deepseek API uses `reasoning_content` instead of `content`"""
#     deepseek_msg = choice["message"]
#     deepseek_msg["reasoning"] = deepseek_msg.pop("reasoning_content")
#     deepseek_msg["finish_reason"] = choice.get("finish_reason", None)
#     return AssistantMessage(**deepseek_msg)


def from_deepseek_assistant_message(choice: dict) -> AssistantMessage:
    """FIXED: make a copy of object and explicitly create data model"""
    deepseek_msg = choice["message"].copy()

    return AssistantMessage(
        role="assistant",
        content=deepseek_msg.get("content"),
        reasoning=deepseek_msg.get("reasoning_content"),
        tool_calls=deepseek_msg.get("tool_calls"),
        finish_reason=choice.get("finish_reason"),
    )
