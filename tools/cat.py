"""Read and output file contents."""
from tools import is_path_safe


def cat(path: str) -> str:
    """Read the contents of a text file.

    >>> with open("test_cat.txt", "w", encoding="utf-8") as f:
    ...     _ = f.write("hello world")
    >>> cat("test_cat.txt")
    'hello world'
    >>> import os
    >>> os.unlink("test_cat.txt")
    >>> cat("nonexistent_file_12345.txt")
    'Error: File not found'
    >>> cat("/etc/passwd")
    'Error: unsafe path'
    """
    if not is_path_safe(path):
        return "Error: unsafe path"

    for encoding in ("utf-8", "utf-16"):
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except FileNotFoundError:
            return "Error: File not found"
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"Error: {e}"
    return "Error: Unicode decode error"