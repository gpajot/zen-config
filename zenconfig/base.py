import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)


class ZenConfigError(Exception):
    """Default error when Handling config files."""


class Format(ABC):
    @classmethod
    @abstractmethod
    def handles(cls, path: Path) -> bool:
        """Return whether the format handles the extension."""

    @abstractmethod
    def load(self, path: Path) -> Dict[str, Any]:
        """Load the configuration file into a dict."""

    @abstractmethod
    def dump(self, path: Path, config: Dict[str, Any]) -> None:
        """Dump in the configuration file."""


C = TypeVar("C")


class Schema(ABC, Generic[C]):
    @classmethod
    @abstractmethod
    def handles(cls, config_class: type) -> bool:
        """Return whether the schema handles the config."""

    @abstractmethod
    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        """Load the schema based on a dict configuration."""

    @abstractmethod
    def to_dict(self, config: Any) -> Dict[str, Any]:
        """Dump the config to dict."""


class BaseConfig(ABC):
    ENV_PATH: ClassVar[str] = "CONFIG"
    PATH: ClassVar[Optional[str]] = None
    _PATHS: ClassVar[Optional[Tuple[Path, ...]]] = None

    FORMATS: ClassVar[List[Type[Format]]] = []
    FORMAT: ClassVar[Optional[Format]] = None

    SCHEMAS: ClassVar[List[Type[Schema]]] = []
    SCHEMA: ClassVar[Optional[Schema]] = None

    @classmethod
    def register_format(cls, format_class: Type[Format]) -> None:
        cls.FORMATS.append(format_class)

    @classmethod
    def register_schema(cls, schema_class: Type[Schema]) -> None:
        cls.SCHEMAS.append(schema_class)

    @classmethod
    def _paths(cls) -> Tuple[Path, ...]:
        if cls._PATHS:
            return cls._PATHS
        found_path: Optional[str] = None
        if cls.ENV_PATH:
            found_path = os.environ.get(cls.ENV_PATH)
        if not found_path:
            found_path = cls.PATH
        if not found_path:
            raise ZenConfigError(
                f"could not find the config path for config {cls.__qualname__}, tried env variable {cls.ENV_PATH}"
            )
        cls._PATHS = tuple(_handle_globbing(Path(found_path).expanduser().absolute()))
        return cls._PATHS

    @classmethod
    def _format(cls, path: Optional[Path] = None) -> Format:
        if cls.FORMAT:
            return cls.FORMAT
        if path:
            _path = path
        else:
            paths = cls._paths()
            if len(paths) != 1:
                raise ZenConfigError(
                    "multiple configuration files, use the path parameter"
                )
            _path = paths[0]
        for format_class in cls.FORMATS:
            if not format_class.handles(_path):
                continue
            fmt = format_class()
            if not path:
                cls.FORMAT = fmt
            return fmt
        raise ZenConfigError(
            f"unsupported config file {path.name} for config {cls.__qualname__}, maybe you are missing an extra"  # type: ignore
        )

    @classmethod
    def _schema(cls) -> Schema:
        if cls.SCHEMA:
            return cls.SCHEMA
        for schema_class in cls.SCHEMAS:
            if not schema_class.handles(cls):
                continue
            cls.SCHEMA = schema_class()
            return cls.SCHEMA
        raise ZenConfigError(
            f"could not infer config schema for config {cls.__qualname__}, maybe you are missing an extra"
        )


def _handle_globbing(original_path: Path) -> Iterator[Path]:
    directory = Path(original_path)
    glob = False
    while "*" in directory.name or "?" in directory.name or "[" in directory.name:
        directory = directory.parent
        glob = True
    if not glob:
        yield original_path
    else:
        for path in directory.rglob(str(original_path.relative_to(directory))):
            if path.is_file():
                yield path
