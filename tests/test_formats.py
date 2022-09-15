from dataclasses import dataclass
from typing import ClassVar

import pytest

from zenconfig.formats.json import JSONFormat
from zenconfig.formats.toml import TOMLFormat
from zenconfig.formats.yaml import YAMLFormat
from zenconfig.schemas.dataclass import DataclassSchema
from zenconfig.write import Config


@dataclass
class BaseConfig(Config):
    PATH: ClassVar[str] = "test_config_file"
    SCHEMA: ClassVar[DataclassSchema] = DataclassSchema()

    a: str
    b: int


@pytest.mark.parametrize(
    "fmt",
    [
        JSONFormat(),
        TOMLFormat(),
        YAMLFormat(),
    ],
)
def test_all_formats(fmt):
    @dataclass
    class FmtConfig(BaseConfig):
        FORMAT = fmt

    cfg = FmtConfig(a="a", b=1)
    cfg.save()
    reloaded = FmtConfig.load()
    assert reloaded.a == "a"
    assert reloaded.b == 1
    cfg.clear()
