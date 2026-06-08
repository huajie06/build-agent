import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

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

response_dict = response.model_dump()

with open("openai_response_test02.json", "w", encoding="utf-8") as file:
    json.dump(response_dict, file, indent=4, ensure_ascii=False)


# choice = response.choices[0]

# # Check if the model wants to call a tool
# if choice.finish_reason == "tool_calls":
#     tool_call = choice.message.tool_calls[0]
#     print(f"Tool requested: {tool_call.function.name}")
#     print(f"Arguments: {tool_call.function.arguments}")

#     args = json.loads(tool_call.function.arguments)
#     expression = args["expression"]
#     result = eval(expression)

#     print(f"Result: {expression} = {result}")

#     messages.append(choice.message)
#     messages.append(
#         {
#             "role": "tool",
#             "content": json.dumps({"result": result}),
#             "tool_call_id": tool_call.id,
#         }
#     )

#     final = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=messages,
#         tools=tools,
#         temperature=0.0,
#     )
#     print(f"Final answer: {final.choices[0].message.content}")
# else:
#     print(f"Answer: {choice.message.content}")
