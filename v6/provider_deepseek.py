from models import Message, AssistantMessage, ToolCall
import json


def to_deepseek_tool_call(tool_call: ToolCall) -> dict:
    return {
        "id": tool_call.id,
        "type": "function",
        "function": {"name": tool_call.name, "arguments": json.dumps(tool_call.args)},
    }


def to_deepseek_message(message: Message) -> dict:
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
            result["tool_calls"] = [
                to_deepseek_tool_call(tool_call) for tool_call in message.tool_calls
            ]

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


def from_deepseek_tool_call(tool_call_data: dict) -> ToolCall:
    function_data = tool_call_data["function"]
    return ToolCall(
        id=tool_call_data["id"],
        name=function_data["name"],
        args=json.loads(function_data["arguments"]),
    )


def from_deepseek_assistant_message(choice: dict) -> AssistantMessage:
    deepseek_msg = choice["message"].copy()

    raw_tool_calls = deepseek_msg.get("tool_calls")
    tool_calls = None
    if raw_tool_calls:
        tool_calls = [
            from_deepseek_tool_call(tool_call) for tool_call in raw_tool_calls
        ]

    return AssistantMessage(
        role="assistant",
        content=deepseek_msg.get("content"),
        reasoning=deepseek_msg.get("reasoning_content"),
        tool_calls=tool_calls,
        finish_reason=choice.get("finish_reason"),
    )
