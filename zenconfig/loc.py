import os
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path


@dataclass
class Loc:
    env: str | None = None
    default: str | None = None

    @cached_property
    def path(self) -> Path:
        found_path: str | None = None
        if self.env:
            found_path = os.environ.get(self.env)
        if not found_path:
            found_path = self.default
        if not found_path:
            raise ValueError(f"could not find the config path for {self!r}")
        return Path(found_path)
