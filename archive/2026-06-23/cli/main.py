import sys
import os
from dotenv import load_dotenv

# Crucial line: ensures Python can resolve the sibling folders properly
# when running from inside the cli directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.runtime import AgentRuntime

load_dotenv()


def start_interactive_session():
    print("====================================")
    print("   Modular Pi-Agent (Python Edition) ")
    print("====================================\n")

    runtime = AgentRuntime()

    user_prompt = input("What would you like to build or learn?\n> ")
    if user_prompt.strip():
        runtime.execute(user_prompt)


if __name__ == "__main__":
    start_interactive_session()
