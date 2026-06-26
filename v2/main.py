"""only CLI"""

from agent import run_agent
from session import save_session, load_session
from pathlib import Path


def cli_loop():
    current_dir = Path(__file__).resolve().parent
    session_file = current_dir / "sessions" / "session.json"

    if session_file.is_file():
        messages = load_session(session_file)

    # bug fix after grade #1
    if messages is None:
        messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        user_input = input("> ").strip()

        # bug fix after grade #1
        if not user_input:
            print("Enter a message")
            continue

        if user_input.lower() == "/exit":
            save_session(messages=messages, path=session_file)
            print("bye")
            break

        messages.append({"role": "user", "content": user_input})
        result = run_agent(messages=messages)

        # bug fix after grade #1
        if result is None:
            print("agent failed")
            continue

        print(result)
        messages.append({"role": "assistant", "content": result})


if __name__ == "__main__":
    cli_loop()
