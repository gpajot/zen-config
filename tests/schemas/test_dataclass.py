from dataclasses import dataclass
from typing import ClassVar

from zenconfig.schemas.dataclass import DataclassSchema
from zenconfig.write import Config


@dataclass
class DeeperConfig:
    d: bool


@dataclass
class DeepConfig:
    c: bool
    deeper: DeeperConfig


@dataclass
class DataclassConfig(Config):
    PATH: ClassVar[str] = "test.json"

    a: str
    b: int
    deep: DeepConfig


def test_dataclass():
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
