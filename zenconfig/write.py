from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar, TypeVar

from zenconfig.read import ReadOnlyConfig, ReadOnlyFormat, ReadOnlySchema


class Format(ReadOnlyFormat, ABC):
    @abstractmethod
    def dump(self, path: Path, config: dict[str, Any]) -> None:
        """Dump in the configuration file."""


C = TypeVar("C")


class Schema(ReadOnlySchema[C], ABC):
    @abstractmethod
    def to_dict(self, config: Any) -> dict[str, Any]:
        """Dump the config to dict."""


class Config(ReadOnlyConfig, ABC):
    FORMAT: ClassVar[Format]
    SCHEMA: ClassVar[Schema]

    FILE_MODE: ClassVar[int] = 0o600

    def save(self) -> None:
        """Save the current config to the file."""
        if not self.path().exists():
            self.path().touch(mode=self.FILE_MODE)
        self.FORMAT.dump(self.path(), self.SCHEMA.to_dict(self))

    def clear(self) -> None:
        """Remove the config file."""
        self.path().unlink(missing_ok=True)
