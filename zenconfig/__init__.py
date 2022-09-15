from typing import ClassVar

from zenconfig.formats.json import JSONFormat
from zenconfig.loc import Loc
from zenconfig.read import ReadOnlyConfig, ReadOnlyFormat, ReadOnlySchema
from zenconfig.schemas.dataclass import DataclassSchema
from zenconfig.write import Config, Format, Schema


class DefaultReadOnlyConfig(Config):
    FORMAT: ClassVar[Format] = JSONFormat()
    SCHEMA: ClassVar[Schema] = DataclassSchema()


class DefaultConfig(DefaultReadOnlyConfig):
    ...
