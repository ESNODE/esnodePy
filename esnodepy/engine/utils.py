import os
import subprocess
import tempfile
from contextlib import contextmanager
from typing import Iterator
from urllib.parse import urlparse


def is_url(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in ("http", "https") and parsed.netloc != ""


@contextmanager
def TargetResolver(target: str) -> Iterator[str]:
    """Context manager that yields an absolute local path for a target.

    If `target` is a URL (http/https) this will `git clone` it into a
    temporary directory and yield that path. If `target` is a local path
    it validates existence and yields the absolute path.

    Raises RuntimeError on clone failures or if local path is invalid.
    """
    if is_url(target):
        tmpdir = tempfile.TemporaryDirectory()
        dest = tmpdir.name
        try:
            subprocess.run(["git", "clone", "--depth", "1", target, dest], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            tmpdir.cleanup()
            raise RuntimeError(f"Failed to clone {target}: {e}") from e
        try:
            yield dest
        finally:
            tmpdir.cleanup()
    else:
        abs_path = os.path.abspath(target or ".")
        if not os.path.exists(abs_path):
            raise RuntimeError(f"Path does not exist: {abs_path}")
        yield abs_path
