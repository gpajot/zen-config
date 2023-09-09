from typing import ClassVar

from pydantic import BaseModel

from tests.schemas.utils import AnEnum, parametrize_formats
from zenconfig.schemas.pydantic import PydanticSchema
from zenconfig.write import Config


class DeeperPydanticConfig(BaseModel):
    d: bool
    e: AnEnum


class DeepPydanticConfig(BaseModel):
    c: bool
    deeper: DeeperPydanticConfig


@parametrize_formats
def test_pydantic(fmt, path):
    class PydanticConfig(Config, BaseModel):
        PATH: ClassVar[str] = path

        a: str
        b: int
        deep: DeepPydanticConfig

    assert isinstance(PydanticConfig._format(), fmt)
    assert isinstance(PydanticConfig._schema(), PydanticSchema)
    cfg = PydanticConfig(
        a="a",
        b=1,
        deep=DeepPydanticConfig(
            c=False,
            deeper=DeeperPydanticConfig(d=True, e=AnEnum.ONE),
        ),
    )
    cfg.save()
    reloaded = PydanticConfig.load()
    assert reloaded.a == "a"
    assert reloaded.b == 1
    assert reloaded.deep.c is False
    assert reloaded.deep.deeper.d is True
    assert reloaded.deep.deeper.e is AnEnum.ONE
    cfg.clear()
