from dataclasses import dataclass
from typing import ClassVar

from tests.schemas.utils import parametrize_formats
from zenconfig.schemas.dataclass import DataclassSchema
from zenconfig.write import Config


@dataclass
class DeeperConfig:
    d: bool


@dataclass
class DeepConfig:
    c: bool
    deeper: DeeperConfig


@parametrize_formats
def test_dataclass(fmt, path):
    @dataclass
    class DataclassConfig(Config):
        PATH: ClassVar[str] = path

        a: str
        b: int
        deep: DeepConfig

    assert isinstance(DataclassConfig._format(), fmt)
    assert isinstance(DataclassConfig._schema(), DataclassSchema)
    cfg = DataclassConfig(
        a="a",
        b=1,
        deep=DeepConfig(
            c=False,
            deeper=DeeperConfig(d=True),
        ),
    )
    cfg.save()
    reloaded = DataclassConfig.load()
    assert reloaded.a == "a"
    assert reloaded.b == 1
    assert reloaded.deep.c is False
    assert reloaded.deep.deeper.d is True
    cfg.clear()
