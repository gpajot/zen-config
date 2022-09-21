from typing import ClassVar

from attrs import define, field

from tests.schemas.utils import AnEnum, encoders, parametrize_formats
from zenconfig.schemas.attrs import AttrsSchema
from zenconfig.write import Config


@define
class DeeperConfig:
    d: bool
    e: AnEnum = field(converter=AnEnum)


@define
class DeepConfig:
    c: bool
    deeper: DeeperConfig


@parametrize_formats
def test_attrs(fmt, path):
    @define
    class AttrsConfig(Config):
        PATH: ClassVar[str] = path
        ENCODERS = encoders

        a: str
        b: int
        deep: DeepConfig

    assert isinstance(AttrsConfig._format(), fmt)
    assert isinstance(AttrsConfig._schema(), AttrsSchema)
    cfg = AttrsConfig(
        a="a",
        b=1,
        deep=DeepConfig(
            c=False,
            deeper=DeeperConfig(d=True, e=AnEnum.ONE),
        ),
    )
    cfg.save()
    reloaded = AttrsConfig.load()
    assert reloaded.a == "a"
    assert reloaded.b == 1
    assert reloaded.deep.c is False
    assert reloaded.deep.deeper.d is True
    assert reloaded.deep.deeper.e is AnEnum.TWO
    cfg.clear()
