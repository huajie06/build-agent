def write_file(filename: str, content: str) -> str:
    """Saves text content into a local file workspace."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"[SUCCESS] File saved as {filename}"
    except Exception as e:
        return f"[ERROR] Failed to write file: {str(e)}"

# The schema map lives alongside the function
WRITE_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Saves structured learning curriculums or notes to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["filename", "content"],
            "additionalProperties": False
        }
    }
}