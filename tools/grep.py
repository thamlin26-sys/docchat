"""Search files using regular expressions."""
import glob
import re
from tools import is_path_safe


def grep(regex: str, path: str) -> str:
    """Search files matching glob path for regex pattern.

    >>> with open("test_sample.txt", "w", encoding="utf-8") as f:
    ...     _ = f.write("TODO: fix bug\\nDone\\nTODO: write tests\\n")
    >>> grep("TODO", "test_sample.txt")
    'TODO: fix bug\\nTODO: write tests'
    >>> import os
    >>> os.unlink("test_sample.txt")
    >>> grep("TODO", "/etc/passwd")
    'Error: unsafe path'
    """
    if not is_path_safe(path):
        return "Error: unsafe path"

    matches = []
    matched_files = glob.glob(path)
    for file_path in sorted(matched_files):
        if not is_path_safe(file_path):
            continue
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if re.search(regex, line):
                        matches.append(line.rstrip("\r\n"))
        except Exception:
            continue

    return "\n".join(matches)