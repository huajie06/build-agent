from pathlib import Path


# tools
def read_text_file(path: str) -> str:
    """Read and return the contents of a UTF-8 text file."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    return file_path.read_text(encoding="utf-8")


def write_text_file(path: str, content: str) -> str:
    """Write UTF-8 text to a file, replacing any existing content."""
    file_path = Path(path)

    # Create parent directories when necessary.
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(content, encoding="utf-8")

    return f"Wrote {len(content)} characters to {path}"


deepseek_tools = [
    {
        "type": "function",
        "function": {
            "name": "read_text_file",
            "description": "Read the complete contents of a text file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the text file to read.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_text_file",
            "description": (
                "Write content to a text file. "
                "This replaces the file if it already exists."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the text file to write.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Complete text to write into the file.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
]

tool_functions = {
    "read_text_file": read_text_file,
    "write_text_file": write_text_file,
}
