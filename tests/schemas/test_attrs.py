from typing import ClassVar

from attrs import define

from zenconfig.schemas.attrs import AttrsSchema
from zenconfig.write import Config


@define
class DeeperConfig:
    d: bool


@define
class DeepConfig:
    c: bool
    deeper: DeeperConfig


@define
class AttrsConfig(Config):
    PATH: ClassVar[str] = "test.json"

    a: str
    b: int
    deep: DeepConfig


def test_attrs():
    assert isinstance(AttrsConfig._schema(), AttrsSchema)
    cfg = AttrsConfig(
        a="a",
        b=1,
        deep=DeepConfig(
            c=False,
            deeper=DeeperConfig(d=True),
        ),
    )
    cfg.save()
    reloaded = AttrsConfig.load()
    assert reloaded.a == "a"
    assert reloaded.b == 1
    assert reloaded.deep.c is False
    assert reloaded.deep.deeper.d is True
    cfg.clear()
