from pathlib import Path
from typing import Any, Callable

TOOL_FUNCTIONS: dict[str, Callable[..., Any]] = {}
DEEPSEEK_TOOLS: list[dict[str, Any]] = []


def tool(name: str, description: str, parameters: dict[str, Any]):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
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


@tool(
    name="read_text_file",
    description="Read and return the contents of a UTF-8 text file.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the text file.",
            }
        },
        "required": ["path"],
        "additionalProperties": False,
    },
)
def read_text_file(path: str) -> str:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    return file_path.read_text(encoding="utf-8")


@tool(
    name="write_text_file",
    description="Write UTF-8 text to a file, replacing existing content.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Destination file path.",
            },
            "content": {
                "type": "string",
                "description": "Text to write.",
            },
        },
        "required": ["path", "content"],
        "additionalProperties": False,
    },
)
def write_text_file(path: str, content: str) -> str:
    file_path = Path(path)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

    return f"Wrote {len(content)} characters to {path}"
