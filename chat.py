"""Interactive chat REPL supporting tools, slash commands, and built-in help."""

import sys
import os

# Safe tool imports supporting both installed package mode and local execution
try:
    from docchat.tools import calculate, ls, cat, grep
except ImportError:
    from tools import calculate, ls, cat, grep

# Global model client variable (lazy-loaded only on ordinary chat messages)
_model_client = None

def get_model_client():
    """Lazily initialize and return the model client only when sending a chat message.

    >>> client = get_model_client()
    """
    global _model_client
    if _model_client is None:
        # Initialize your LLM client here using os.environ.get("GEMINI_API_KEY") etc.
        pass
    return _model_client

def handle_command(command: str) -> str:
    """Handle slash commands or standard chat inputs.
    
    >>> handle_command("/exit")
    'Goodbye!'
    """
    command = command.strip()
    if command in ("/exit", "exit", "quit"):
        return "Goodbye!"
    if command.startswith("/calc "):
        return str(calculate.calculate(command[6:]))
    if command.startswith("/ls "):
        return str(ls.ls(command[4:]))
    if command.startswith("/cat "):
        return str(cat.cat(command[5:]))
    if command.startswith("/grep "):
        parts = command[6:].split(" ", 1)
        if len(parts) == 2:
            return str(grep.grep(parts[0], parts[1]))
        return "Usage: /grep <pattern> <path>"
    
    # Ordinary chat message: triggers model client initialization
    client = get_model_client()
    return f"Echo: {command}"

def repl():
    """Run the interactive chat REPL loop.

    >>> from unittest.mock import patch
    >>> with patch("builtins.input", side_effect=["/exit"]):
    ...     repl()
    Welcome to docchat! Type /exit to quit.
    Goodbye!
    """
    print("Welcome to docchat! Type /exit to quit.")
    while True:
        try:
            user_input = input("docchat> ")
        except (KeyboardInterrupt, EOFError, OSError):
            print("\nGoodbye!")
            break
        
        response = handle_command(user_input)
        print(response)
        if response == "Goodbye!":
            break

# Expose Chat alias after repl is fully defined
Chat = repl

if __name__ == "__main__":
    repl()
