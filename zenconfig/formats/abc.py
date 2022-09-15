from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Format(ABC):
    @abstractmethod
    def load(self, path: Path) -> dict[str, Any]:
        """Load the configuration file into a dict."""

    @abstractmethod
    def dump(self, path: Path, config: dict[str, Any]) -> None:
        """Dump in the configuration file."""
