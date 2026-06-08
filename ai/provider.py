import os
from openai import OpenAI

class DeepSeekProvider:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.model = "deepseek-v4-flash"

    def query(self, messages: list, tools_schema: list):
        """Pure wrapper to hit the model endpoint."""
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools_schema,
            tool_choice="auto"
        )