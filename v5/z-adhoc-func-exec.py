from tools import TOOL_FUNCTIONS
from models import AssistantMessage
import json

func_call_raw_str = r"""
{
        "role": "assistant",
        "content": "Sure, let me read that file for you!",
        "reasoning": "The user wants me to read a file called \"tools.py\" in the current directory. Let me try to read it.",
        "tool_calls": [
            {
                "index": 0,
                "id": "call_00_dIRH5HS7MPppCPuFAVIj1370",
                "type": "function",
                "function": {
                    "name": "read_text_file",
                    "arguments": "{\"path\": \"./tools.py\"}"
                }
            }
        ],
        "finish_reason": "tool_calls"
    }
"""
data = json.loads(func_call_raw_str)
msg = AssistantMessage(**data)

tool_calls = msg.tool_calls

for tool_call in tool_calls:
    tool_call_id = tool_call["id"]
    function_data = tool_call["function"]

    tool_name = function_data["name"]
    args = json.loads(function_data["arguments"])

    print(f"[Tool requested: {tool_name}]")
    print(f"[Arguments: {args}]")

    function = TOOL_FUNCTIONS.get(tool_name)
    print("-" * 30)
    print(args)
    print(type(args))
    print("-" * 30)
    func_result = function(**args)
    print(func_result)
