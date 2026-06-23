"""
write joke to my current folder, called joke_01.txt

in my current folder, read the agent_v1.py file and summarize it for me
"""

import httpx
from dotenv import load_dotenv
import os
import json
from pathlib import Path

load_dotenv()

token = os.environ["DEEPSEEK_API_KEY"]
print(token)

url = "https://api.deepseek.com/chat/completions"


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

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}",
}


message = [
    {
        "role": "system",
        "content": "You are a helpful assistant",
    }
]


def run_agent(message):
    payload = {
        "messages": message,
        "model": "deepseek-v4-flash",
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "max_tokens": 4096,
        "response_format": {"type": "text"},
        "stream": False,
        "temperature": 1,
        "top_p": 1,
        "tools": deepseek_tools,
        "tool_choice": "auto",
        "logprobs": False,
    }

    loop_counter = 0
    while True:
        if loop_counter >= 5:
            print("hit max iteration")
            return
        try:
            response = httpx.request("POST", url, headers=headers, json=payload)
            loop_counter += 1
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print(
                f"Error {exc.response.status_code} while requesting {exc.request.url}."
            )
            return

        json_resp = response.json()

        choice = json_resp["choices"][0]
        assistant_message = choice["message"]

        if choice.get("finish_reason") == "tool_calls":
            message.append(assistant_message)

            tool_calls = assistant_message.get("tool_calls", [])
            for tool_call in tool_calls:
                tool_call_id = tool_call["id"]
                function_data = tool_call["function"]

                tool_name = function_data["name"]
                args = json.loads(function_data["arguments"])

                print(f"Tool requested: {tool_name}")
                print(f"Arguments: {args}")

                function = tool_functions.get(tool_name)

                if function is None:
                    result = {"error": f"Unknown tool: {tool_name}"}
                else:
                    try:
                        result = function(**args)
                    except Exception as exc:
                        result = {"error": str(exc)}

                message.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(
                            {"result": result},
                            ensure_ascii=False,
                        ),
                    }
                )

        if choice.get("finish_reason") == "stop":
            ai_content = choice["message"]["content"]
            ai_reason_content = choice["message"]["reasoning_content"]
            print("reasons")
            print(ai_reason_content)
            print("-" * 20)
            return ai_content


while True:
    user_input = str(input("enter your question:\n"))
    user_input_text = user_input.strip()

    if user_input_text.lower() == "/exit":
        with open("output.json", "w", encoding="utf-8") as file:
            json.dump(message, file, indent=4)

        print("bye")
        break

    if user_input_text == "":
        print("enter msg")
        continue

    message.append({"role": "user", "content": user_input_text})
    result = run_agent(message)
    print("result")
    print(result)
    print("-" * 20)
    message.append({"role": "assistant", "content": result})
