from enum import Enum
from typing import ClassVar

from pydantic import BaseModel

from zenconfig.schemas.pydantic import PydanticSchema
from zenconfig.write import Config


class AnEnum(Enum):
    ONE = 1
    TWO = 2


class DeeperPydanticConfig(BaseModel):
    d: bool


class DeepPydanticConfig(BaseModel):
    c: bool
    deeper: DeeperPydanticConfig


class PydanticConfig(Config, BaseModel):
    PATH: ClassVar[str] = "test.json"

    class Config:
        json_encoders = {
            # Test if custom encoders are working.
            AnEnum: lambda e: AnEnum.TWO.value,
        }

    a: str
    b: AnEnum
    deep: DeepPydanticConfig


def test_pydantic():
    assert isinstance(PydanticConfig._schema(), PydanticSchema)
    cfg = PydanticConfig(
        a="a",
        b=AnEnum.ONE,
        deep=DeepPydanticConfig(
            c=False,
            deeper=DeeperPydanticConfig(d=True),
        ),
    )
    cfg.save()
    reloaded = PydanticConfig.load()
    assert reloaded.a == "a"
    assert reloaded.b is AnEnum.TWO
    assert reloaded.deep.c is False
    assert reloaded.deep.deeper.d is True
    cfg.clear()
