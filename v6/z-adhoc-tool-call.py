from models import ToolCall
import json
from pathlib import Path


data_path = Path("/home/mz/repos/learning/v5/raw_data/") / "deepseek-raw-tool-call.json"


with data_path.open("r") as f:
    resp = json.load(f)

choice = resp["choices"][0]
msg = choice["message"]
tool_call = msg["tool_calls"][0]

print(tool_call)

tc = ToolCall(
    id=tool_call["id"],
    name=tool_call["function"]["name"],
    args=json.loads(tool_call["function"]["arguments"]),
)

print(tc.args)
print(type(tc.args))
