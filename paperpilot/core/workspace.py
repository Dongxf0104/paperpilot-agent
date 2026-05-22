from __future__ import annotations

from pathlib import Path

from paperpilot.core.io import ensure_dir


class Workspace:
    def __init__(self, root: str | Path = ".") -> None:
        self.root = Path(root)

    def resolve(self, path: str | Path) -> Path:
        candidate = Path(path)
        if candidate.is_absolute():
            return candidate
        return self.root / candidate

    def output_dir(self, name: str = "outputs") -> Path:
        return ensure_dir(self.root / name)
