from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar

C = TypeVar("C")


class Schema(ABC, Generic[C]):
    @abstractmethod
    def from_dict(self, cls: Type[C], cfg: dict[str, Any]) -> C:
        """Load the schema based on a dict configuration."""

    @abstractmethod
    def to_dict(self, config: Any) -> dict[str, Any]:
        """Dump the config to dict."""
