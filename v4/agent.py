from llm import call_DeepSeek
from tools import TOOL_FUNCTIONS
import httpx
import json


def run_agent(messages: list[dict], max_loop_cnt=5) -> str | None:
    """agent loop
    - set up max attempts as 5
    """
    loop_counter = 0

    while True:
        if loop_counter >= max_loop_cnt:
            print("Agent call ends due to reaching max iteration")
            return None
        try:
            result = call_DeepSeek(messages)
        except httpx.HTTPError as exc:
            print(f"Deepseek call failed: {exc}")
            return None

        loop_counter += 1
        choice = result["choices"][0]
        assistant_message = choice["message"]

        if choice.get("finish_reason") == "tool_calls":
            messages.append(assistant_message)

            tool_calls = assistant_message.get("tool_calls", [])
            for tool_call in tool_calls:
                tool_call_id = tool_call["id"]
                function_data = tool_call["function"]

                tool_name = function_data["name"]
                args = json.loads(function_data["arguments"])

                print(f"[Tool requested: {tool_name}]")
                print(f"[Arguments: {args}]")

                function = TOOL_FUNCTIONS.get(tool_name)

                if function is None:
                    func_result = {"error": f"Unknown tool: {tool_name}"}
                else:
                    try:
                        func_result = function(**args)
                    except Exception as exc:
                        func_result = {"error": str(exc)}

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(
                            {"result": func_result},
                            ensure_ascii=False,
                        ),
                    }
                )

        if choice.get("finish_reason") == "stop":
            assistant_content = choice["message"]["content"]
            assistant_reason_content = choice["message"].get("reasoning_content")
            print("[REASONS]")
            print(assistant_reason_content)
            print("-" * 50)
            return assistant_content
