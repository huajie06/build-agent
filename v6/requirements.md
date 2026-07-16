Your next task should be **Milestone 2D: introduce an internal `ToolCall` model**.

You have already separated provider-specific formatting at the message level. The remaining provider-specific structure is inside `AssistantMessage.tool_calls`.

Right now, `agent.py` still understands this external shape:

```python
tool_call["id"]
tool_call["function"]["name"]
tool_call["function"]["arguments"]
```

That means the agent loop still partly depends on DeepSeek/OpenAI-style response dictionaries.

## Goal of 2D

After this milestone, `agent.py` should work only with your own internal models:

```python
tool_call.id
tool_call.name
tool_call.arguments
```

DeepSeek’s nested structure should be understood only by `provider_deepseek.py`.

The boundary becomes:

```text
DeepSeek response
    ↓ provider_deepseek.py
Internal AssistantMessage
    └── list[ToolCall]
            ├── id
            ├── name
            └── arguments
    ↓
agent.py
```

## Task 1: create the internal model

Add this to `models.py`:

```python
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "arguments": self.arguments,
        }
```

Then change:

```python
tool_calls: list[dict] | None = None
```

to:

```python
tool_calls: list[ToolCall] | None = None
```

The architectural purpose is not just prettier syntax. It changes tool calls from **provider data** into **application data**.

## Task 2: parse DeepSeek tool calls in the adapter

DeepSeek currently returns arguments as a JSON string:

```python
{
    "id": "call_123",
    "function": {
        "name": "read_text_file",
        "arguments": "{\"path\": \"notes.txt\"}"
    }
}
```

Convert that into your internal model inside `provider_deepseek.py`:

```python
import json

from models import AssistantMessage, Message, ToolCall
```

Create a focused helper:

```python
def from_deepseek_tool_call(data: dict) -> ToolCall:
    function_data = data["function"]

    return ToolCall(
        id=data["id"],
        name=function_data["name"],
        arguments=json.loads(function_data["arguments"]),
    )
```

Then use it when building the assistant message:

```python
raw_tool_calls = deepseek_msg.get("tool_calls")

tool_calls = None
if raw_tool_calls:
    tool_calls = [
        from_deepseek_tool_call(tool_call)
        for tool_call in raw_tool_calls
    ]

return AssistantMessage(
    role="assistant",
    content=deepseek_msg.get("content"),
    reasoning=deepseek_msg.get("reasoning_content"),
    tool_calls=tool_calls,
    finish_reason=choice.get("finish_reason"),
)
```

Now JSON parsing happens at the provider boundary rather than in the agent.

## Task 3: simplify the agent loop

Replace this:

```python
tool_call_id = tool_call["id"]
function_data = tool_call["function"]

tool_name = function_data["name"]
function = TOOL_FUNCTIONS.get(tool_name)

args = json.loads(function_data["arguments"])
func_result = function(**args)
```

with:

```python
function = TOOL_FUNCTIONS.get(tool_call.name)

if function is None:
    func_result = {
        "error": f"unknown tool requested: {tool_call.name}"
    }
else:
    try:
        func_result = function(**tool_call.arguments)
    except Exception as e:
        func_result = {"error": str(e)}
```

And construct the result with:

```python
ToolMessage(
    role="tool",
    tool_call_id=tool_call.id,
    content=json.dumps(
        {"result": func_result},
        ensure_ascii=False,
    ),
)
```

After this change, `agent.py` should no longer need to import `json` for argument parsing, although it still needs it for encoding the tool result.

## Task 4: support session serialization

Your assistant message cannot directly serialize a list of dataclass objects through `json.dump()`.

Update `AssistantMessage.to_dict()`:

```python
def to_dict(self) -> dict:
    return {
        "role": self.role,
        "content": self.content,
        "reasoning": self.reasoning,
        "tool_calls": (
            [tool_call.to_dict() for tool_call in self.tool_calls]
            if self.tool_calls is not None
            else None
        ),
        "finish_reason": self.finish_reason,
    }
```

Then update session loading so assistant tool calls become `ToolCall` objects again:

```python
def parse_message(data: dict) -> Message:
    role = data.get("role")

    if role == "system":
        return SystemMessage(**data)

    if role == "user":
        return UserMessage(**data)

    if role == "assistant":
        raw_tool_calls = data.get("tool_calls")

        tool_calls = None
        if raw_tool_calls:
            tool_calls = [
                ToolCall(**tool_call)
                for tool_call in raw_tool_calls
            ]

        return AssistantMessage(
            role="assistant",
            content=data.get("content"),
            reasoning=data.get("reasoning"),
            tool_calls=tool_calls,
            finish_reason=data.get("finish_reason"),
        )

    if role == "tool":
        return ToolMessage(**data)

    raise ValueError(f"Unknown message role: {role}")
```

## Task 5: convert internal tool calls back to DeepSeek format

When conversation history is sent back to DeepSeek, your internal `ToolCall` must be converted back into DeepSeek’s nested structure:

```python
def to_deepseek_tool_call(tool_call: ToolCall) -> dict:
    return {
        "id": tool_call.id,
        "type": "function",
        "function": {
            "name": tool_call.name,
            "arguments": json.dumps(tool_call.arguments),
        },
    }
```

Then inside `to_deepseek_message()`:

```python
if message.tool_calls:
    result["tool_calls"] = [
        to_deepseek_tool_call(tool_call)
        for tool_call in message.tool_calls
    ]
```

This completes both directions:

```text
DeepSeek dict → internal ToolCall
internal ToolCall → DeepSeek dict
```

## Completion criteria

You can consider 2D complete when all four cases work:

1. A normal question without tools returns an answer.
2. A request causes one tool call and then a final answer.
3. A request causes multiple tool calls.
4. After saving and restarting, a session containing tool calls loads and continues successfully.

The key test is this:

> `agent.py` should contain no knowledge of `"function"`, `"arguments"` JSON strings, or DeepSeek’s nested tool-call dictionary format.

Do this milestone only. Do not add a generic provider interface, abstract base classes, validation libraries, or async HTTP yet.
