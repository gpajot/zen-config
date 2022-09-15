from abc import ABC
from typing import ClassVar

from zenconfig.read import ReadOnlyConfig


class Config(ReadOnlyConfig, ABC):
    FILE_MODE: ClassVar[int] = 0o600

    def save(self) -> None:
        """Save the current config to the file."""
        if not self._path().exists():
            self._path().touch(mode=self.FILE_MODE)
        self._format().dump(self._path(), self._schema().to_dict(self))

    def clear(self) -> None:
        """Remove the config file."""
        self._path().unlink(missing_ok=True)
