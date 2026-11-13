"""Evaluate arithmetic expressions safely."""
import re


def calculate(expression: str) -> str:
    """Evaluate a safe arithmetic expression.

    >>> calculate("2 + 2 * 3")
    '8'
    >>> calculate("(10 - 2) / 4")
    '2.0'
    >>> calculate("import os")
    'Error: invalid characters in expression'
    """
    if not re.match(r'^[\d\s\+\-\*\/\%\.\(\)]+$', expression):
        return "Error: invalid characters in expression"
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"
        """
>>> calculate("1 / 0")
'Error: invalid characters in expression'
"""
        
