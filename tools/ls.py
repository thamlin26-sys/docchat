"""List directory contents."""
import glob
import os
from tools import is_path_safe


def ls(path: str = ".") -> str:
    """List files in a directory asciibetically.

    >>> os.makedirs("test_dir", exist_ok=True)
    >>> open(os.path.join("test_dir", "b.txt"), "w").close()
    >>> open(os.path.join("test_dir", "a.txt"), "w").close()
    >>> ls("test_dir").splitlines()
    ['a.txt', 'b.txt']
    >>> import shutil
    >>> shutil.rmtree("test_dir")
    >>> ls("/etc")
    'Error: unsafe path'
    """
    if not is_path_safe(path):
        return "Error: unsafe path"

    if os.path.isdir(path):
        pattern = os.path.join(path, "*")
    else:
        pattern = path

    files = glob.glob(pattern)
    basenames = [os.path.basename(f) or f for f in files]
    return "\n".join(sorted(basenames))
