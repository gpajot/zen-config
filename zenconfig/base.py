import os
from abc import ABC
from pathlib import Path
from typing import ClassVar, List, Union

from zenconfig.formats.abc import Format
from zenconfig.formats.selectors import FormatSelector, format_selectors
from zenconfig.schemas.abc import Schema
from zenconfig.schemas.selectors import SchemaSelector, schema_selectors


class BaseConfig(ABC):
    ENV_PATH: ClassVar[str] = "CONFIG"
    PATH: ClassVar[Union[str, None]] = None
    _PATH: ClassVar[Union[Path, None]] = None

    FORMATS: ClassVar[List[FormatSelector]] = format_selectors
    FORMAT: ClassVar[Union[Format, None]] = None

    SCHEMAS: ClassVar[List[SchemaSelector]] = schema_selectors
    SCHEMA: ClassVar[Union[Schema, None]] = None

    @classmethod
    def _path(cls) -> Path:
        if cls._PATH:
            return cls._PATH
        found_path: Union[str, None] = None
        if cls.ENV_PATH:
            found_path = os.environ.get(cls.ENV_PATH)
        if not found_path:
            found_path = cls.PATH
        if not found_path:
            raise ValueError(
                f"could not find the config path for config {cls.__qualname__}, tried env variable {cls.ENV_PATH}"
            )
        cls._PATH = Path(found_path).expanduser().absolute()
        return cls._PATH

    @classmethod
    def _format(cls) -> Format:
        if cls.FORMAT:
            return cls.FORMAT
        ext = cls._path().suffix
        for selector in cls.FORMATS:
            fmt = selector(ext)
            if fmt:
                cls.FORMAT = fmt
                return fmt
        raise ValueError(
            f"unsupported config file extension {ext} for config {cls.__qualname__}"
        )

    @classmethod
    def _schema(cls) -> Schema:
        if cls.SCHEMA:
            return cls.SCHEMA
        for selector in cls.SCHEMAS:
            schema = selector(cls)
            if schema:
                cls.SCHEMA = schema
                return schema
        raise ValueError(
            f"could not infer config schema for config {cls.__qualname__}, maybe you are missing an extra"
        )
