from typing import ClassVar

import pytest

from zenconfig.formats.json import JSONFormat
from zenconfig.formats.toml import TOMLFormat
from zenconfig.formats.yaml import YAMLFormat
from zenconfig.schemas.dict import DictSchema
from zenconfig.write import Config


class BaseConfig(Config, dict):
    PATH: ClassVar[str] = "test_config_file"
    SCHEMA: ClassVar[DictSchema] = DictSchema()


@pytest.mark.parametrize(
    "fmt",
    [
        JSONFormat(),
        TOMLFormat(),
        YAMLFormat(),
    ],
)
def test_all_formats(fmt):
    class FmtConfig(BaseConfig):
        FORMAT = fmt

    cfg = FmtConfig(a="a", b=1)
    cfg.save()
    reloaded = FmtConfig.load()
    assert reloaded == {"a": "a", "b": 1}
    cfg.clear()
