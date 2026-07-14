from models import Message, ToolMessage
from llm import call_llm
from tools import TOOL_FUNCTIONS
import json


def run_agent(messages: list[Message], max_loop_cnt=3):

    loop_cnt = 0

    while True:
        if loop_cnt >= max_loop_cnt:
            print(f"agent reaches max counter: {loop_cnt}")
            return None

        try:
            assistant_msg_result = call_llm(messages)
        except Exception as e:
            print(f"call_llm() failed due to {e}")
            return None

        loop_cnt += 1

        if assistant_msg_result.finish_reason == "tool_calls":
            # FIXED: if a reponse fail to provide actual `tool_calls`
            if not assistant_msg_result.tool_calls:
                print("provider returned tool_calls finish reason without tool calls")
                return None

            messages.append(assistant_msg_result)

            tool_calls = assistant_msg_result.tool_calls
            for tool_call in tool_calls:
                tool_call_id = tool_call["id"]
                function_data = tool_call["function"]

                tool_name = function_data["name"]
                function = TOOL_FUNCTIONS.get(tool_name)

                if function is None:
                    func_result = {"error": f"unknown tool requested: {tool_name}"}
                else:
                    try:
                        # FIXED: if model supplies invalid JSON
                        args = json.loads(function_data["arguments"])
                        func_result = function(**args)
                    except Exception as e:
                        func_result = {"error": str(e)}
                        print(f"function {function} error: {func_result}")

                messages.append(
                    ToolMessage(
                        role="tool",
                        tool_call_id=tool_call_id,
                        content=json.dumps({"result": func_result}, ensure_ascii=False),
                    )
                )
            continue

        elif assistant_msg_result.finish_reason == "stop":
            print("[REASONING]")
            print(assistant_msg_result.reasoning)
            print("-" * 50)
            return assistant_msg_result

        else:
            print(f"Unsupported finish reason: {assistant_msg_result.finish_reason}")
            # FIXED: add None return
            return None
