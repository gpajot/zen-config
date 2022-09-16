import contextlib
import os
from abc import ABC
from dataclasses import is_dataclass
from pathlib import Path
from typing import ClassVar, Type, TypeVar, Union

from zenconfig.formats.abc import Format
from zenconfig.schemas.abc import Schema

C = TypeVar("C", bound="ReadOnlyConfig")


class ReadOnlyConfig(ABC):
    ENV_PATH: ClassVar[Union[str, None]] = None
    PATH: ClassVar[Union[str, None]] = None
    _PATH: ClassVar[Union[Path, None]] = None

    FORMAT: ClassVar[Union[Format, None]] = None
    SCHEMA: ClassVar[Union[Schema, None]] = None

    @classmethod
    def _path(cls) -> Path:
        if not cls._PATH:
            found_path: Union[str, None] = None
            if cls.ENV_PATH:
                found_path = os.environ.get(cls.ENV_PATH)
            if not found_path:
                found_path = cls.PATH
            if not found_path:
                raise ValueError(
                    f"could not find the config path for config {cls.__qualname__}"
                )
            cls._PATH = Path(found_path).expanduser()
        return cls._PATH

    @classmethod
    def _format(cls) -> Format:
        if cls.FORMAT:
            return cls.FORMAT
        suffix = cls._path().suffix
        if suffix == ".json":
            from zenconfig.formats.json import JSONFormat

            return JSONFormat()
        if suffix in {".yml", ".yaml"}:
            with contextlib.suppress(ImportError):
                from zenconfig.formats.yaml import YAMLFormat

                return YAMLFormat()
        if suffix == ".toml":
            with contextlib.suppress(ImportError):
                from zenconfig.formats.toml import TOMLFormat

                return TOMLFormat()
        raise ValueError(
            f"unsupported config file extension {suffix} for config {cls.__qualname__}, maybe you should require an extra"
        )

    @classmethod
    def _schema(cls) -> Schema:
        if cls.SCHEMA:
            return cls.SCHEMA
        if is_dataclass(cls):
            from zenconfig.schemas.dataclass import DataclassSchema

            return DataclassSchema()
        if issubclass(cls, dict):
            from zenconfig.schemas.dict import DictSchema

            return DictSchema()
        with contextlib.suppress(ImportError):
            from pydantic import BaseModel

            if issubclass(cls, BaseModel):
                from zenconfig.schemas.pydantic import PydanticSchema

                return PydanticSchema()
        raise ValueError(
            f"could not infer config schema for config {cls.__qualname__}, maybe you should require an extra"
        )

    @classmethod
    def load(cls: Type[C]) -> C:
        return cls._schema().from_dict(cls, cls._format().load(cls._path()))
