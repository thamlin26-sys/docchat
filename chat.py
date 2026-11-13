"""DocChat interactive conversational assistant with tool support."""
import json
import os
from dotenv import load_dotenv
from groq import Groq
from tools.calculate import calculate
from tools.ls import ls
from tools.cat import cat
from tools.grep import grep

load_dotenv()

FUNCTIONS = {
    "calculate": calculate,
    "ls": ls,
    "cat": cat,
    "grep": grep,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate an arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ls",
            "description": "List files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cat",
            "description": "Read the contents of a text file.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "Search files using regular expressions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "regex": {"type": "string"},
                    "path": {"type": "string"},
                },
                "required": ["regex", "path"],
            },
        },
    },
]


class Chat:
    """Manages chat state, conversation history, and tool execution with Groq LLM.

    >>> import os
    >>> os.environ["GROQ_API_KEY"] = "offline-test"
    >>> chat = Chat()
    >>> len(chat.messages)
    0
    """

    def __init__(self, model="llama3-8b-8192"):
        """Initialize Chat instance with API client and empty history."""
        self.model = model
        self.messages = []
        self.client = None

    def _get_client(self):
        if self.client is None:
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY", "offline-test"))
        return self.client

    def send_message(self, prompt: str, temperature: float = 0.7) -> str:
        """Send a message to the model, handle tool calls automatically, and return response.

        >>> import os
        >>> os.environ["GROQ_API_KEY"] = "offline-test"
        >>> chat = Chat()
        >>> class MockChoice:
        ...     def __init__(self, message):
        ...         self.message = message
        >>> class MockMessage:
        ...     def __init__(self, content, tool_calls=None):
        ...         self.content = content
        ...         self.tool_calls = tool_calls
        ...     def model_dump(self, exclude_none=True):
        ...         return {"role": "assistant", "content": self.content}
        >>> class MockResponse:
        ...     def __init__(self, message):
        ...         self.choices = [MockChoice(message)]
        >>> chat._get_client().chat.completions.create = lambda *args, **kwargs: MockResponse(MockMessage("Tool result handled"))
        >>> chat.send_message("Hello", temperature=0)
        'Tool result handled'
        """
        self.messages.append({"role": "user", "content": prompt})
        client = self._get_client()

        while True:
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=TOOLS,
                    temperature=temperature
                )
                message = response.choices[0].message
            except Exception as e:
                return f"Error: {e}"

            if getattr(message, "tool_calls", None):
                asst_msg = message.model_dump(exclude_none=True)
                asst_msg["role"] = "assistant"
                self.messages.append(asst_msg)

                for call in message.tool_calls:
                    name = call.function.name
                    try:
                        args = json.loads(call.function.arguments)
                    except Exception:
                        args = {}

                    if name in FUNCTIONS:
                        result = str(FUNCTIONS[name](**args))
                    else:
                        result = f"Error: Unknown tool {name}"

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result,
                    })
            else:
                reply = message.content or ""
                self.messages.append({"role": "assistant", "content": reply})
                return reply


def repl(temperature: float = 0.8):
    """Run the interactive Read-Eval-Print Loop supporting manual slash commands."""
    chat = Chat()
    while True:
        try:
            user_input = input("chat> ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            break

        stripped = user_input.strip()
        if not stripped:
            continue

        if stripped.startswith("/"):
            parts = stripped[1:].split(maxsplit=1)
            cmd = parts[0]
            arg = parts[1] if len(parts) > 1 else ""

            if cmd in FUNCTIONS:
                try:
                    if cmd == "ls" and not arg:
                        res = FUNCTIONS[cmd]()
                    elif cmd == "calculate":
                        res = FUNCTIONS[cmd](arg)
                    elif cmd == "cat":
                        res = FUNCTIONS[cmd](arg)
                    elif cmd == "grep":
                        grep_parts = arg.split(maxsplit=1)
                        if len(grep_parts) == 2:
                            res = FUNCTIONS[cmd](grep_parts[0], grep_parts[1])
                        else:
                            res = "Error: grep requires <regex> <path>"
                    else:
                        res = FUNCTIONS[cmd](arg)
                except Exception as e:
                    res = f"Error: {e}"

                print(res)
                chat.messages.append({"role": "user", "content": user_input})
                chat.messages.append({"role": "assistant", "content": str(res)})
            else:
                print(f"Unknown command: /{cmd}")
            continue

        reply = chat.send_message(stripped, temperature=temperature)
        print(reply)


if __name__ == "__main__":
    repl()
