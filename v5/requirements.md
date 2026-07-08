Nice. Then your **2B milestone** is basically:

You now understand that your **internal message model** should preserve more than just:

```python
role
content
```

Because assistant messages may also contain:

```python
reasoning
tool_calls
finish_reason
provider-specific metadata
```

And tool result messages need:

```python
tool_call_id
name
content/result
```

So the next step is not “add more random fields.” The next step is to make the architecture cleaner.

## Next step: Phase 2C — Provider Boundary Conversion

The goal of **2C** is:

> Keep your internal session format stable, then convert it to/from DeepSeek/OpenAI/Anthropic format only at the boundary.

In other words:

```text
Your app/session model
        ↓
provider adapter
        ↓
DeepSeek API format
```

And after response:

```text
DeepSeek response
        ↓
provider adapter
        ↓
Your app/session model
```

This prevents the rest of your agent from becoming tightly coupled to DeepSeek’s exact JSON shape.

## What to build next

Create a file like:

```text
providers/
  deepseek.py
```

or, simpler for now:

```text
provider_deepseek.py
```

Inside it, make two functions:

```python
def to_deepseek_messages(messages: list[Message]) -> list[dict]:
    ...
```

and:

```python
def from_deepseek_assistant_message(choice: dict) -> AssistantMessage:
    ...
```

The first one converts your internal messages into API request messages.

The second one converts the API response back into your internal model.

## Concrete task

Start with only these internal message types:

```python
UserMessage
AssistantMessage
ToolMessage
```

Something like:

```python
@dataclass
class UserMessage:
    role: Literal["user"]
    content: str


@dataclass
class AssistantMessage:
    role: Literal["assistant"]
    content: str | None = None
    reasoning: str | None = None
    tool_calls: list[dict] | None = None
    finish_reason: str | None = None


@dataclass
class ToolMessage:
    role: Literal["tool"]
    tool_call_id: str
    content: str
    name: str | None = None
```

Then define the union:

```python
Message = UserMessage | AssistantMessage | ToolMessage
```

Your session should save/load `list[Message]`, not `list[dict]`.

## Why this is the right next step

You already found the key bug:

```text
session replay breaks because assistant/tool details are lost
```

So now you want the session layer to preserve the full conversation state.

But you do **not** want your whole app to think in raw DeepSeek dictionaries. That would make it harder later when you add another model provider.

So the design should be:

```text
main.py
  owns app loop

session.py
  saves/loads internal Message objects

models.py
  defines UserMessage, AssistantMessage, ToolMessage

llm.py
  calls provider adapter + sends request

provider_deepseek.py
  converts internal messages <-> DeepSeek API shape

tools.py
  executes tool calls
```

## Suggested 2C implementation order

Do it in this order:

### 1. Update `models.py`

Define your message dataclasses.

Do not worry about every possible provider field yet. Just preserve the important ones.

### 2. Update `session.py`

Make `save_session()` serialize dataclasses to JSON.

Make `load_session()` reconstruct dataclasses from JSON.

The key idea is that each saved object needs a discriminator, usually `role`.

Example saved JSON:

```json
[
  {
    "role": "user",
    "content": "summarize this file"
  },
  {
    "role": "assistant",
    "content": null,
    "reasoning": "I need to read the file first.",
    "tool_calls": [
      {
        "id": "call_123",
        "type": "function",
        "function": {
          "name": "read_text_file",
          "arguments": "{\"path\": \"notes.txt\"}"
        }
      }
    ],
    "finish_reason": "tool_calls"
  },
  {
    "role": "tool",
    "tool_call_id": "call_123",
    "name": "read_text_file",
    "content": "{\"result\": \"file content here\"}"
  }
]
```

### 3. Update `llm.py`

Before calling DeepSeek:

```python
api_messages = to_deepseek_messages(messages)
```

After receiving response:

```python
assistant_msg = from_deepseek_assistant_message(choice)
messages.append(assistant_msg)
```

### 4. Update tool execution

When assistant response has tool calls:

```python
for tool_call in assistant_msg.tool_calls:
    ...
    messages.append(ToolMessage(...))
```

Then call the model again with the updated messages.

## Your next mental model

The agent loop should now feel like this:

```text
1. user enters input
2. append UserMessage
3. call LLM
4. append AssistantMessage
5. if AssistantMessage has tool_calls:
      execute tools
      append ToolMessage for each result
      call LLM again
6. append final AssistantMessage
7. save full session
```

This is the moment where your project starts looking like a real agent rather than a single API wrapper.

## My recommendation

For 2C, do **not** add streaming yet.

Do **not** add multiple providers yet.

Do **not** redesign the tool system yet.

Just make this true:

> I can quit the app after a tool call conversation, restart it, load the session, and the model still understands what happened.

That is the success test for 2C.
