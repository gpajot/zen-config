import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar, Generic, Type, TypeVar


class ReadOnlyFormat(ABC):
    @abstractmethod
    def load(self, path: Path) -> dict[str, Any]:
        """Load the configuration file into a dict."""


C = TypeVar("C")


class ReadOnlySchema(ABC, Generic[C]):
    @abstractmethod
    def from_dict(self, cls: Type[C], cfg: dict[str, Any]) -> C:
        """Load the schema based on a dict configuration."""


CC = TypeVar("CC", bound="ReadOnlyConfig")


class ReadOnlyConfig(ABC):
    ENV_PATH: ClassVar[str | None] = None
    PATH: ClassVar[str | None] = None
    _PATH: ClassVar[Path | None] = None

    FORMAT: ClassVar[ReadOnlyFormat]
    SCHEMA: ClassVar[ReadOnlySchema]

    @classmethod
    def path(cls) -> Path:
        if not cls._PATH:
            found_path: str | None = None
            if cls.ENV_PATH:
                found_path = os.environ.get(cls.ENV_PATH)
            if not found_path:
                found_path = cls.PATH
            if not found_path:
                raise ValueError("could not find the config path")
            cls._PATH = Path(found_path)
        return cls._PATH

    @classmethod
    def load(cls: Type[CC]) -> CC:
        return cls.SCHEMA.from_dict(cls, cls.FORMAT.load(cls.path()))
