Many tutorials would immediately jump to "memory" or "RAG". I'd rather spend one phase on a seemingly simple refactor because it teaches an important architectural pattern.

## What did you actually learn?

On the surface, yes, you replaced:

```python
tool_functions = {
    "read_text_file": read_text_file,
    ...
}

deepseek_tools = [
    ...
]
```

with a decorator.

But the real lesson is much deeper.

Before, you had **three sources of truth**:

```python
def read_text_file(...):
```

↓

```python
tool_functions = {
    "read_text_file": read_text_file
}
```

↓

```python
deepseek_tools = [
    ...
]
```

Every time you added a tool, you had to update **three places**.

That's brittle.

Now, the function itself is the source of truth. When Python imports `tools.py`, each decorated function automatically registers itself into both registries.

That is called **self-registration**.

---

## Why do frameworks use this?

Almost every mature framework does something similar.

For example:

### Flask

```python
@app.route("/hello")
def hello():
    ...
```

The decorator registers the route.

---

### pytest

```python
@pytest.fixture
def db():
    ...
```

The decorator registers the fixture.

---

### Click

```python
@click.command()
def main():
    ...
```

Registers a CLI command.

---

### FastAPI

```python
@app.get("/users")
def users():
    ...
```

Registers an endpoint.

---

### Your agent

```python
@tool(...)
def read_text_file(...):
```

Registers a tool.

It's the same architectural idea.

---

## I reviewed your implementation

I think it's very clean.

Things I like:

* `TOOL_FUNCTIONS` and `DEEPSEEK_TOOLS` are built automatically.
* `llm.py` no longer knows how tools are registered—it just consumes `DEEPSEEK_TOOLS`.
* `agent.py` just looks up `TOOL_FUNCTIONS`; it doesn't care how they were populated.

That's a nice separation of concerns.

---

## One tiny improvement

Right now you're passing the tool name twice:

```python
@tool(
    name="read_text_file",
)
def read_text_file(...):
```

Those two names can drift apart accidentally.

Later, we'll simplify the decorator to infer the name automatically:

```python
@tool(
    description="Read a UTF-8 text file.",
    parameters={...},
)
def read_text_file(...):
```

and inside the decorator:

```python
name = func.__name__
```

We'll also eventually infer parts of the schema from the function signature and docstring. That's how libraries like Pydantic AI and Pi reduce boilerplate. But I **wouldn't** do that yet—you've reached a good stopping point where everything is still explicit and easy to understand.

---

## I think you've finished Phase 2A

At this point your project has a respectable architecture:

```text
CLI
    │
    ▼
Agent Loop
    │
    ▼
LLM
    │
    ▼
Tool Registry
    │
    ▼
Python Functions
```

There's nothing I'd ask you to refactor before moving on.

### My recommendation for Phase 2B

The next phase should **not** be more tools.

Instead, introduce your **first internal data model** using `@dataclass`.

Right now, everything in your agent is still a raw `dict`:

```python
{"role": "user", "content": "..."}
```

That's fine for a prototype, but it's the point where I'd start introducing domain models like `Message`, `ToolCall`, and `ToolResult`.

This is a much bigger architectural step than adding another tool, and it lays the foundation for supporting multiple LLM providers later. I think it's the most valuable next milestone.
