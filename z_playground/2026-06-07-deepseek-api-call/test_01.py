import json
from openai import OpenAI
from dotenv import load_dotenv
from typing import Any
import os

model = "deepseek-v4-flash"
base_url = "https://api.deepseek.com"

system_prompt = "you are a helpful assistant"
user_query = "hi! how are you today"


load_dotenv()

messages: list[dict[str, Any]] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_query},
]

# api_key = os.environ.get("DEEPSEEK_API_KEY")
# print(api_key)

client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url=base_url)

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.0,
    extra_body={"thinking": {"type": "disabled"}},
)

response_dict = response.model_dump()

with open("openai_response.json", "w", encoding="utf-8") as file:
    json.dump(response_dict, file, indent=4, ensure_ascii=False)
