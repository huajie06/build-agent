from pathlib import Path
from agent import run_agent
from session import load_session, save_session
from models import SystemMessage, UserMessage

INITIAL_MESSAGE = SystemMessage(role="system", content="you are a helpful agent")


def cli_loop():
    current_dir = Path(__file__).resolve().parent
    session_file = current_dir / "session" / "session.json"

    if session_file.is_file():
        messages = load_session(str(session_file))
    else:
        messages = None

    if messages is None:
        messages = [INITIAL_MESSAGE]

    while True:
        user_input = input("> ").strip()

        if user_input.lower() == "/exit":
            save_session(data=messages, path=str(session_file))
            print("bye")
            break

        messages.append(UserMessage(role="user", content=user_input))

        result = run_agent(messages=messages)

        if result is None:
            print("agent failed")
            continue

        print(result.content)
        messages.append(result)


if __name__ == "__main__":
    cli_loop()
