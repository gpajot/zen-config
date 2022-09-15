from typing import ClassVar

import pytest

from zenconfig.formats.json import JSONFormat
from zenconfig.formats.toml import TOMLFormat
from zenconfig.formats.yaml import YAMLFormat
from zenconfig.write import Config


class BaseConfig(Config, dict):
    ...


@pytest.mark.parametrize(
    ("fmt", "ext"),
    [
        (JSONFormat, ".json"),
        (TOMLFormat, ".toml"),
        (YAMLFormat, ".yaml"),
    ],
)
def test_all_formats(fmt, ext):
    class FmtConfig(BaseConfig):
        PATH: ClassVar[str] = f"test_config_file{ext}"

    # Check format inference works.
    assert isinstance(FmtConfig._format(), fmt)

    cfg = FmtConfig(a="a", b=1)
    cfg.save()
    reloaded = FmtConfig.load()
    assert reloaded == {"a": "a", "b": 1}
    cfg.clear()
