import json
import sys
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    print("Error: DEEPSEEK_API_KEY not set in environment")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate, e.g. '2 + 3 * 4'",
                    }
                },
                "required": ["expression"],
            },
        },
    }
]

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant with access to a calculator tool. Use it when the user asks for math calculations.",
    },
    {"role": "user", "content": "What is (25 + 37) * 12?"},
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,
    temperature=0.0,
)


choice = response.choices[0]

if choice.finish_reason == "tool_calls":
    messages.append(choice.message.model_dump())

    for tool_call in choice.message.tool_calls:
        print(f"Tool requested: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")

        args = json.loads(tool_call.function.arguments)
        expression = args["expression"]
        result = eval(expression)

        print(f"Result: {expression} = {result}")

        messages.append(
            {
                "role": "tool",
                "content": json.dumps({"result": result}),
                "tool_call_id": tool_call.id,
            }
        )

    with open("test_03_messages.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)

    final = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        temperature=0.0,
    )
    print(f"Final answer: {final.choices[0].message.content}")

    with open("test_03_final_response.json", "w", encoding="utf-8") as f:
        json.dump(final.model_dump(), f, indent=4, ensure_ascii=False)

else:
    print(f"Answer: {choice.message.content}")
