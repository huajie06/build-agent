Next step: **Phase 2A — clean tool registry**.

Goal: replace this manual mapping:

```python
tool_functions = {
    "read_text_file": read_text_file,
    "write_text_file": write_text_file,
}
```

with a decorator:

```python
@tool
def read_text_file(path: str) -> str:
    ...
```

Target outcome:

```python
TOOL_FUNCTIONS
DEEPSEEK_TOOLS
```

are built automatically.

Start with this in `tools.py`:

```python
from pathlib import Path
from typing import Callable, Any

TOOL_FUNCTIONS: dict[str, Callable[..., Any]] = {}
DEEPSEEK_TOOLS: list[dict] = []


def tool(name: str, description: str, parameters: dict):
    def decorator(func: Callable[..., Any]):
        TOOL_FUNCTIONS[name] = func

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

        return func

    return decorator
```

Then rewrite one tool like:

```python
@tool(
    name="read_text_file",
    description="Read the complete contents of a UTF-8 text file.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path of the text file to read.",
            }
        },
        "required": ["path"],
    },
)
def read_text_file(path: str) -> str:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    return file_path.read_text(encoding="utf-8")
```

Then update imports:

```python
# llm.py
from tools import DEEPSEEK_TOOLS
```

```python
# agent.py
from tools import TOOL_FUNCTIONS
```

This teaches one important agent-framework idea:

```text
Tool definition = Python function + LLM schema + registry entry
```

Once you finish this, show me `tools.py`, `llm.py`, and `agent.py`.
