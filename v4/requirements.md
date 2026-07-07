Perfect. This is actually one of my favorite phases because it's where your code stops being "JSON everywhere" and starts becoming an application.

## Phase 2B — Internal Data Model

The goal is **not** to use dataclasses because they're "Pythonic."

The goal is to separate your **internal representation** from the **LLM provider's representation**.

This is an important idea used by nearly every mature agent framework.

---

# The Principle

Right now your application uses DeepSeek's JSON format everywhere:

```python
{
    "role": "user",
    "content": "Hello"
}
```

That means your entire application is coupled to one provider.

Instead, think of it like this:

```text
          Your Agent
────────────────────────────────

 Message
 ToolCall
 ToolResult
 Session

────────────────────────────────
        Conversion Layer
────────────────────────────────

 DeepSeek JSON

 OpenAI JSON

 Anthropic JSON

 Gemini JSON
```

Notice something:

Your agent should **never care** how DeepSeek formats messages.

That's `llm.py`'s job.

---

# Why This Matters

Imagine next month you decide to support OpenAI.

Today you'd have to search your entire project for:

```python
message["role"]
```

or

```python
message["content"]
```

because every file knows the provider format.

Instead:

```python
Message(
    role="user",
    content="Hello"
)
```

Everything else stays identical.

Only `llm.py` changes.

---

# What We'll Build

Don't over-engineer it.

One file:

```text
models.py
```

Start with only one class.

```python
from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str
```

That's it.

Nothing else.

---

Then make one helper.

```python
def to_dict(self) -> dict:
    return {
        "role": self.role,
        "content": self.content,
    }
```

Now your agent owns the model.

DeepSeek only receives

```python
message.to_dict()
```

---

# What Not to Build Yet

Don't make

```python
Tool
ToolSchema
ToolRegistry
AssistantMessage
UserMessage
SystemMessage
```

No inheritance.

No generics.

No base classes.

No Pydantic.

We're intentionally keeping the model tiny.

---

# The Next Refactor

Currently you have

```python
messages: list[dict]
```

Eventually we want

```python
messages: list[Message]
```

Notice how much nicer this becomes.

Instead of

```python
messages.append(
    {
        "role": "user",
        "content": text,
    }
)
```

you write

```python
messages.append(
    Message(
        role="user",
        content=text,
    )
)
```

Then, inside `llm.py`:

```python
payload = {
    "messages": [
        message.to_dict()
        for message in messages
    ]
}
```

The conversion to the provider format happens in exactly one place.

---

# Why We're Doing It This Way

You may remember a few weeks ago we discussed having classes like:

* `Message`
* `ToolCall`
* `ToolResult`

At the time, I suggested not implementing them yet because they would have added complexity before you had a working agent.

Now the timing is right.

Your agent already:

* chats
* loops
* executes tools
* persists sessions
* has a clean architecture

So introducing an internal model now simplifies the design instead of complicating it.

---

# Scope for This Milestone

I want to keep it intentionally small:

* Create `models.py`.
* Implement only `Message`.
* Add `to_dict()` and `from_dict()` methods.
* Change the application to use `list[Message]` internally.
* Let `llm.py` handle conversion to DeepSeek's JSON format.
* Keep the tool messages as plain dictionaries for now.

Once that's working, we'll review it together. After that, the next step will be extending the model to cover tool calls and tool results, and you'll start to see how providers differ while your agent code stays almost unchanged.
