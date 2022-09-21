from enum import Enum

import pytest

from zenconfig.encoder import Encoders
from zenconfig.formats.json import JSONFormat
from zenconfig.formats.toml import TOMLFormat
from zenconfig.formats.yaml import YAMLFormat

parametrize_formats = pytest.mark.parametrize(
    ("fmt", "path"),
    [
        (JSONFormat, "test.json"),
        (TOMLFormat, "test.toml"),
        (YAMLFormat, "test.yaml"),
    ],
)


class AnEnum(Enum):
    ONE = 1
    TWO = 2


encoders: Encoders = {
    # Test if custom encoders are working.
    AnEnum: lambda e: AnEnum.TWO.value,
}
