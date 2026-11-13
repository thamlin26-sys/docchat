"""Tools package for docchat."""


def is_path_safe(path: str) -> bool:
    """Return True if path is relative and does not contain directory traversal steps.

    >>> is_path_safe("notes.txt")
    True
    >>> is_path_safe("/etc/passwd")
    False
    >>> is_path_safe("../secret.txt")
    False
    >>> is_path_safe("docs/../secret.txt")
    False
    """
    if path.startswith("/"):
        return False
    parts = path.split("/")
    if ".." in parts:
        return False
    return True