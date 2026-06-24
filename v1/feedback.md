---
title: "feedback from GPT"
date: 2026-06-23
---


Yes — before moving to next phase, I would refactor this. Not “production production,” but **clean Phase 1/2 foundation**.

Main issues to fix first:

1. **Do not print API token**

```python
print(token)  # remove
```

2. **Rename `message` to `messages`**

It is a list, so plural helps mentally.

3. **Separate concerns**

Right now one file does:

```text
env loading
LLM request
tool definitions
tool schema
tool execution
agent loop
CLI loop
session saving
```

That is too much.

4. **Add HTTP timeout**

```python
httpx.post(..., timeout=60)
```

5. **Handle missing `reasoning_content` safely**

```python
choice["message"].get("reasoning_content")
```

6. **Do not append `None` as assistant message**

If `run_agent()` fails, this line is dangerous:

```python
message.append({"role": "assistant", "content": result})
```

Guard it.

---

## Recommended next refactor

Use this structure:

```text
agent_v1/
├── main.py
├── config.py
├── llm.py
├── tools.py
├── agent.py
├── session.py
└── sessions/
```

Keep it simple.

---

## Responsibility split

### `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-flash"
```

---

### `tools.py`

Put:

```python
read_text_file()
write_text_file()
deepseek_tools
tool_functions
```

here.

Later we can improve this with decorators.

---

### `llm.py`

One job: call DeepSeek.

```python
def call_llm(messages: list[dict]) -> dict:
    ...
```

No agent loop here.

---

### `agent.py`

One job: agent loop.

```python
def run_agent(messages: list[dict]) -> str | None:
    ...
```

This file handles:

```text
assistant response
tool call detection
tool execution
tool result append
final answer return
```

---

### `session.py`

```python
def save_session(messages, path="sessions/session.json"):
    ...

def load_session(path):
    ...
```

---

### `main.py`

Only CLI:

```python
messages = [{"role": "system", "content": "You are a helpful assistant."}]

while True:
    user_input = input("> ").strip()
    ...
```

---

## One important conceptual note

You currently call this Phase 1, but your code already includes **tool calling**, which is Phase 2.

So I’d rename your current status as:

```text
Phase 1.5 — Chat loop + rough tool loop
```

Your next milestone should be:

```text
Phase 1.5 Refactor
```

Success criteria:

```text
- no API token print
- no giant single file
- clean llm.py / tools.py / agent.py / main.py split
- session save works
- read/write tools still work
- total code still small
```

Do **not** add decorators yet.
Do **not** add dataclasses yet unless you want to.
Do **not** add memory yet.

First make the current version clean and understandable.
