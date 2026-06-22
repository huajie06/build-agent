import httpx
import dotenv
import os
import json

dotenv.load_dotenv()

token = os.environ["DEEPSEEK_API_KEY"]
print(token)


url = "https://api.deepseek.com/chat/completions"

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


payload = {
    "messages": [
        {"content": "You are a helpful assistant", "role": "system"},
        {
            "content": "Hi, can you summarize my file at current folder: abc.py",
            "role": "user",
        },
    ],
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
    "tool_choice": "auto",
    "logprobs": False,
    "top_logprobs": None,
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}",
}

response = httpx.request("POST", url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
