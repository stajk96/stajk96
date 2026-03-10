"""Launch helper for IDE users (e.g., Spyder) to avoid running patch text as Python."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    cmd = [sys.executable, "-m", "streamlit", "run", str(root / "app.py")]
    return subprocess.call(cmd, cwd=str(root))


if __name__ == "__main__":
    raise SystemExit(main())
