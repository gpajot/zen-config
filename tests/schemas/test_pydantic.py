from typing import ClassVar

from pydantic import BaseModel

from zenconfig.formats.json import JSONFormat
from zenconfig.schemas.pydantic import PydanticSchema
from zenconfig.write import Config


class DeeperPydanticConfig(BaseModel):
    d: bool


class DeepPydanticConfig(BaseModel):
    c: bool
    deeper: DeeperPydanticConfig


class PydanticConfig(Config, BaseModel):
    PATH: ClassVar[str] = "test.json"
    FORMAT: ClassVar[JSONFormat] = JSONFormat()
    SCHEMA: ClassVar[PydanticSchema] = PydanticSchema()

    a: str
    b: int
    deep: DeepPydanticConfig


def test_pydantic():
    cfg = PydanticConfig(
        a="a",
        b=1,
        deep=DeepPydanticConfig(
            c=False,
            deeper=DeeperPydanticConfig(d=True),
        ),
    )
    cfg.save()
    reloaded = PydanticConfig.load()
    assert reloaded.a == "a"
    assert reloaded.b == 1
    assert reloaded.deep.c is False
    assert reloaded.deep.deeper.d is True
    cfg.clear()
