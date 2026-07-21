## Next milestone: **2E — make tool definitions provider-independent**

You have removed DeepSeek-specific structure from messages and tool calls. The remaining provider coupling is now in `tools.py`:

```python
DEEPSEEK_TOOLS: list[dict[str, Any]] = []
```

and:

```python
DEEPSEEK_TOOLS.append(
    {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters,
        },
    }
)
```

The tool registry currently does two jobs:

1. Registers executable Python functions.
2. Builds DeepSeek-specific API dictionaries.

The second responsibility should move to `provider_deepseek.py`.

## Design goal

After 2E, your application should store tools using its own internal representation:

```text
ToolDefinition
├── name
├── description
└── parameters
```

Then the DeepSeek adapter converts that representation at the API boundary:

```text
Internal ToolDefinition
        ↓
provider_deepseek.py
        ↓
DeepSeek tool schema
```

This follows the same pattern you already established for messages:

```text
Internal Message → DeepSeek message
Internal ToolCall → DeepSeek tool call
Internal ToolDefinition → DeepSeek tool definition
```

## Task 1: add `ToolDefinition`

In `models.py`, add:

```python
from typing import Any


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]
```

You do not necessarily need `to_dict()` because this model is not currently being saved in the session.

## Task 2: update the tool registry

In `tools.py`, replace:

```python
DEEPSEEK_TOOLS: list[dict[str, Any]] = []
```

with:

```python
TOOL_DEFINITIONS: list[ToolDefinition] = []
```

Then update the decorator:

```python
def tool(name: str, description: str, parameters: dict[str, Any]):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        TOOL_FUNCTIONS[name] = func

        TOOL_DEFINITIONS.append(
            ToolDefinition(
                name=name,
                description=description,
                parameters=parameters,
            )
        )

        return func

    return decorator
```

The decorator should now know nothing about DeepSeek.

## Task 3: add the provider conversion

In `provider_deepseek.py`, add:

```python
from models import ToolDefinition


def to_deepseek_tool_definition(tool: ToolDefinition) -> dict:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters,
        },
    }
```

For the complete list:

```python
def to_deepseek_tool_definitions(
    tools: list[ToolDefinition],
) -> list[dict]:
    return [
        to_deepseek_tool_definition(tool)
        for tool in tools
    ]
```

## Task 4: update `llm.py`

Replace:

```python
from tools import DEEPSEEK_TOOLS
```

with:

```python
from tools import TOOL_DEFINITIONS
```

Import the adapter function:

```python
from provider_deepseek import (
    to_deepseek_messages,
    to_deepseek_tool_definitions,
    from_deepseek_assistant_message,
)
```

Then construct the provider tools:

```python
api_tools = to_deepseek_tool_definitions(TOOL_DEFINITIONS)
```

and use:

```python
"tools": api_tools,
```

## Expected files to change

Only these files should need changes:

```text
models.py
tools.py
provider_deepseek.py
llm.py
```

You should not need to change:

```text
agent.py
session.py
main.py
config.py
```

## Completion condition

The most important check is:

> Searching the project for `DEEPSEEK_TOOLS` should return no results.

And `tools.py` should contain no DeepSeek-specific names or API structure.

Your agent should still successfully:

1. Receive a normal response.
2. Invoke `read_text_file`.
3. Invoke `write_text_file`.
4. Send the tool result back and receive a final answer.

This milestone completes the provider-independent data boundary for both **messages** and **tools**.
