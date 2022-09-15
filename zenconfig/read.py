from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar, Type, TypeVar

from zenconfig.loc import Loc


class ReadOnlyFormat(ABC):
    @abstractmethod
    def load(self, path: Path) -> dict[str, Any]:
        """Load the configuration file into a dict."""


C = TypeVar("C")


class ReadOnlySchema(ABC):
    @abstractmethod
    def from_dict(self, cls: Type[C], cfg: dict[str, Any]) -> C:
        """Load the schema based on a dict configuration."""


CC = TypeVar("CC", bound="ReadOnlyConfig")


class ReadOnlyConfig(ABC):
    LOC: ClassVar[Loc]

    FORMAT: ClassVar[ReadOnlyFormat]
    SCHEMA: ClassVar[ReadOnlySchema]

    @classmethod
    def load(cls: Type[CC]) -> CC:
        return cls.SCHEMA.from_dict(cls, cls.FORMAT.load(cls.LOC.path))
