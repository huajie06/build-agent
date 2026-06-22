from pathlib import Path
import httpx
import dotenv
import os
import json

# env
dotenv.load_dotenv()
token = os.environ["DEEPSEEK_API_KEY"]


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


tool_functions = {
    "read_text_file": read_text_file,
    "write_text_file": write_text_file,
}

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

default_messge = [
    {"content": "You are a helpful assistant", "role": "system"},
    {"content": "Hi", "role": "user"},
]


def send_to_deepseek(message=default_messge):
    url = "https://api.deepseek.com/chat/completions"

    payload = {
        "messages": message,
        "model": "deepseek-v4-flash",
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "max_tokens": 4096,
        "response_format": {"type": "text"},
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": 1,
        "top_p": 1,
        "tools": deepseek_tools,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None,
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = httpx.request("POST", url, headers=headers, json=payload)
    return response


my_message = [{"role": "system", "content": "you are a helpful assistant."}]

while True:
    user_input = str(input("enter your question: "))
    user_input_text = user_input.strip()

    if user_input_text.lower() == "/exit":
        print("bye")
        break

    if user_input_text == "":
        print("enter msg")
        continue

    my_message.append({"role": "user", "content": user_input_text})
    resp = send_to_deepseek(my_message)
    resp.raise_for_status()
    json_resp = resp.json()

    choice = json_resp["choices"][0]

    ai_content = choice["message"]["content"]
    ai_reason_content = choice["message"]["reasoning_content"]
    ai_finish_reason = choice["finish_reason"]
    ai_tool_calls = choice["tool_calls"]

    if ai_finish_reason == "tool_calls":
        for tool_call in ai_tool_calls:
            print(f"Tool requested: {tool_call.function.name}")
            print(f"Arguments: {tool_call.function.arguments}")

            args = json.loads(tool_call.function.arguments)
            tool_name = tool_call.function.name
            function = tool_functions[tool_name]
            result = function(**args)

            my_message.append(
                {
                    "role": "tool",
                    "content": json.dumps({"result": result}),
                    "tool_call_id": tool_call.id,
                }
            )

        
