from pathlib import Path
import json

file_path = (
    Path("/Users/hzhang/repos/build-agent/z_playground/2026-06-07-deepseek-api-call")
    / "openai_response_test02.json"
)


with open(file_path) as f:
    data = json.load(f)

# print(json.dumps(data, indent=2))

print(data["choices"][0]["finish_reason"])
print(data["choices"][0]["message"])
