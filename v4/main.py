"""only CLI"""

from agent import run_agent
from session import save_session, load_session
from pathlib import Path
from models import Message


def cli_loop():
    current_dir = Path(__file__).resolve().parent
    session_file = current_dir / "sessions" / "session.json"

    if session_file.is_file():
        messages = load_session(session_file)
    else:
        messages = None

    if messages is None:
        messages = [Message(role="system", content="You are a helpful assistant")]

    while True:
        user_input = input("> ").strip()

        if not user_input:
            print("Enter a message")
            continue

        if user_input.lower() == "/exit":
            save_session(messages=messages, path=session_file)
            print("bye")
            break

        messages.append(Message(role="user", content=user_input))
        result = run_agent(messages=messages)

        if result is None:
            print("agent failed")
            continue

        print(result)
        messages.append(Message(role="assistant", content=result))


if __name__ == "__main__":
    cli_loop()
